import serial


class Belan(object):
    '''
    Класс анализатора спектра Белан СК4 - Белан 32
    Зададим функции для работы по интерфесу RS-232
    '''
    # Открытие порта
    ser = serial.Serial('/dev/ttyUSB0', 9600, stopbits=2, timeout=1)
    ser.close()

    # Декоратором будем проверять готовность com порта
    def check_com_port(func):

        def _wrapper(self, *args, **kwargs):
            '''
            Так как буфер команд не очищается самостоятельно,
            то перед отправкой каждой команды и после ее отправки
            будем вручную считывать все символы находящиееся в буфере
            с помощью команды readline(), она читает все символы до /n
            соответственно, в конце каждой отправленной команды,
            ,будем отправлять символ /n
            На текущий момент не все команды вписан этот символ,
            так как спектроанализатор на некоторые команды самостоятельно
            отправляет в конце своего сообщения симвло /n,
            т.к. на него не было нормальной документации,
            методом проб и ошибок было установлно, но требует проверки,
            что если в конце команды, отправленной генератору ставить ';',
            то ответ он завершит /n, но это не точно,
            пока что все работает
            '''
            self.ser.open()  # Открытие порта
            if self.ser.isOpen():  # Проверка порта
                self.ser.write(b'\n')
                self.ser.readline()
                znach = func(self, *args, **kwargs)  # Обработка команды
                self.ser.write(b'\n')
                self.ser.readline()
                self.ser.close()
            else:
                print("Error, com port is not aviable")
            return znach
        return _wrapper

    # Считывание экрана спектроанализатора
    @check_com_port
    def read_graf(self):
        '''
        Если перед считывание графика не поставить однокртаную разверту
        то спектроанализатор может вернуть неверные данные
        поэтому перед принятием этих данных, настроена их проверка
        ( она достаточно простая)
        Через рекурсию максимум 5 попыток считывание
        Иначе команда возвращает False
        При установке однократной развертки, такой ошибки не наблюдалось
        При однкратной развертке, перед каждым полученим графика,
        настроено обновление экрана спектроанализатора
        '''
        for i in range(5):  # Пытаемся до 5 раз
            # Следующая развертка (обновляет экран)
            self.next_razr()
            self.ser.readline()  # Очистка буфера
            self.ser.write(b':trace:data? trace1;\n')  # Отправка команды
            self.ser.readline()  # Очистка буфера
            buffer = self.ser.readline()  # Чтение данных
            '''
            Здесь очитка принимает такой вид,
            пусть в буфере в худшем случае лежит такая строка
            com1/ncom_next_razr/ncom_get_data/ndata/ncom2/n
            тогда com1/n очистит декоратор
            com_next_raxr/n самостоятельно очистим перед отправкой команды на чтение
            com_get_data/n самостоятельно очистим после отправки команды на чтение
            data/n прочитаем и положим в буффер
            com2/n очистит декоратор
            '''
            buffer = buffer.split()  # Так спектроанализатор возвращает в битовом виде
            # То декодируем в цикле
            for i in range(len(buffer)):
                buffer[i] = buffer[i].decode('utf-8')
                y_lvl = list(map(float, buffer))
                # Проверка данных
                if min(y_lvl) < -2000 or y_lvl[0] > -1:
                    continue  # Если не получилось - повторяем попытку
                else:
                    return y_lvl  # Если получилось - возвращаем данные

        return False # Если не удалось после 5 попыток - возвращаем False

    # Установка частоты
    @check_com_port
    def inst_cent_freq(self, freq):
        _string = ':sense:freq:cent {} Hz;'.format(freq)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    # Проверка ответа, на '*IDN?;' возвращает свое название
    @check_com_port
    def chek_belan(self, *args, **kwargs):
        _string = '*IDN?;'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        return self.ser.readline()

    # Команда смены развертки на одкр/многокр.
    @check_com_port
    def set_razv(self, rej):
        if rej is True:
            rej = 0
        else:
            rej = 1
        _string = ':INITiate:CONTinuous {};'.format(rej)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        self.next_razr()

    # Установка маркера
    # Метод очистки такой же
    @check_com_port
    def set_marker(self):
        self.next_razr()
        self.ser.readline()
        _string = ':trac:math:peak;\n'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        self.ser.readline()
        buffer = self.ser.readline()
        buffer = buffer.split()
        freq, ampl = list(map(float, buffer))
        return freq, ampl

    # Команда обновление экрана - развертки
    def next_razr(self):
        _string = ':INITiate:IMMediate;'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    # Возвращает ось x спектроанализатора
    @check_com_port
    def polosa_x(self):
        # Начало оси
        _string = ':sens:freq:start ?;\n'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        buffer = self.ser.readline()
        buffer = self.ser.readline()
        x_start = float(buffer.decode('utf-8')[:-2])
        # Конец оси
        _string = ':sens:freq:stop ?;\n'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        buffer = self.ser.readline()
        buffer = self.ser.readline()
        x_stop = float(buffer.decode('utf-8')[:-2])
        # Сколько всего точек
        _string = ':Sense:Sweep:Points ?;\n'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        buffer = self.ser.readline()
        buffer = self.ser.readline()
        N_otch = int(buffer.decode('utf-8'))

        return x_start, x_stop, N_otch

    # Установка полосы обзора
    @check_com_port
    def set_span(self, span_bw):
        _string = ':SENSe:FREQ:SPAN {} Hz;'.format(span_bw)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    # Устанвка полосы пропускания частотного фильтра
    @check_com_port
    def set_res(self, radio_bw):
        _string = ':sens:band:res {} Hz;'.format(radio_bw)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    # Установка полосы видеофильтра
    @check_com_port
    def set_video_filtr(self, video_bw):
        _string = ':sense:band:video {} Hz;'.format(video_bw)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)


# BelCmd(3) = ":sense:pow:range " + Replace((CStr(ACH.Oporn_BEL)), ",", ".") + "dBm;" 'установка опорного уровня
# BelCmd(4) = ":sense:pow:rf:att 10;"        'установка аттенюатора

