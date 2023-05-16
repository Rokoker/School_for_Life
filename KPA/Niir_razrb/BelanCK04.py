import serial


class Belan(object):
    '''
    Класс анализатора спектра Белан СК4 - Белан 32
    Зададим функции для работы по интерфесу RS-232
    '''

    ser = serial.Serial('/dev/ttyUSB0', 9600, stopbits=2, timeout=1)
    ser.close()

    # Декоратором будем проверять готовность com порта
    def check_com_port(func):

        def _wrapper(self, *args, **kwargs):

            self.ser.open()
            if self.ser.isOpen():
                self.ser.write(b'\n')
                self.ser.readline()
                znach = func(self, *args, **kwargs)
                self.ser.write(b'\n')
                self.ser.readline()
                self.ser.close()
            else:
                print("Error, com port is not aviable")
            return znach
        return _wrapper

    @check_com_port
    def read_graf(self):
            for i in range(5): # пытаемся до 5 раз
                self.next_razr()
                self.ser.readline()
                self.ser.write(b':trace:data? trace1;\n')
                self.ser.readline()
                buffer = self.ser.readline()

                buffer = buffer.split()

                for i in range(len(buffer)):
                    buffer[i] = buffer[i].decode('utf-8')
                y_lvl = list(map(float, buffer))
                if min(y_lvl)<-2000 or y_lvl[0]>-1:
                    continue # если не получилось - повторяем попытку
                else:
                    return y_lvl  # если получилось - возвращаем данные

            return False # если не удалось после 5 попыток - возвращаем False

    @check_com_port
    def inst_cent_freq(self, freq):
        _string = ':sense:freq:cent {} Hz;'.format(freq)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    @check_com_port
    def chek_belan(self, *args, **kwargs):
        _string = '*IDN?;'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        return self.ser.readline()

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

    @check_com_port
    def set_marker(self):
        self.next_razr()
        self.ser.readline()
        _string = ':trac:math:peak;\n'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        buffer = self.ser.readline()
        buffer = self.ser.readline()
        buffer = buffer.split()
        freq, ampl = list(map(float, buffer))
        return freq, ampl

    def next_razr(self):
        _string = ':INITiate:IMMediate;'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    @check_com_port
    def polosa_x(self):
        _string = ':sens:freq:start ?;\n'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        buffer = self.ser.readline()
        buffer = self.ser.readline()
        x_start = float(buffer.decode('utf-8')[:-2])

        _string = ':sens:freq:stop ?;\n'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        buffer = self.ser.readline()
        buffer = self.ser.readline()
        x_stop = float(buffer.decode('utf-8')[:-2])

        _string = ':Sense:Sweep:Points ?;\n'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        buffer = self.ser.readline()
        buffer = self.ser.readline()
        N_otch = int(buffer.decode('utf-8'))

        return x_start, x_stop, N_otch

    @check_com_port
    def set_span(self, span_bw):
        _string = ':SENSe:FREQ:SPAN {} Hz;'.format(span_bw)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    @check_com_port
    def set_res(self, radio_bw):
        _string = ':sens:band:res {} Hz;'.format(radio_bw)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    @check_com_port
    def set_video_filtr(self, video_bw):
        _string = ':sense:band:video {} Hz;'.format(video_bw)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)


# BelCmd(3) = ":sense:pow:range " + Replace((CStr(ACH.Oporn_BEL)), ",", ".") + "dBm;" 'установка опорного уровня
# BelCmd(4) = ":sense:pow:rf:att 10;"        'установка аттенюатора

