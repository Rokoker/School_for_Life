import pyvisa as visa


# Класс для работы с генераторм сигнала Agilent


class Agilent(object):
    rm = visa.ResourceManager()  # Через pyvisa выводим список всех устройств
    # dev = list(rm.list_resources())
    # Открываем сессию, с Agilent, USB0...::INSTR - адрес генератора
    my_instrument = rm.open_resource("USB0::2391::8216::0115001392::0::INSTR")
    my_instrument.close()  # Закрываем сессию

    # Декоратором перед запуском каждой команды,
    # будет проверять готовность генератора
    def check_session(func):

        def _wrapper(self, *args, **kwargs):
            self.my_instrument.open()  # Открываем сессию
            if self.my_instrument.session:  # Проверяем сессию
                znach = func(self, *args, **kwargs)  # Обрабатывем функцию
                self.my_instrument.close()  # Закрываем сессию

            else:
                print("Error, Agilent N9310A is not aviable")
            return znach
        return _wrapper

    # Проверка установки соединения с генератором
    # На команду "*IDN?" он отправит свое название
    @check_session
    def check_agilent(self):
        _string = self.my_instrument.query("*IDN?")
        return _string

    # Установка амплитуды
    @check_session
    def set_amplitude(self, ampl):
        self.my_instrument.write(":AMPLitude:CW {} dBm".format(ampl))

    # Включение или отключение выхода радиочастоты
    # False - выключить, True - включить
    @check_session
    def rf_out_stat(self, param):
        self.my_instrument.write(":RFOutput:STATe {}".format(param))

    # Выключнеие модуляции
    @check_session
    def mod_stat(self):
        self.my_instrument.write(":MOD:STATe OFF")

    # Установка частоты несущей
    @check_session
    def set_freq(self, F):
        self.my_instrument.write(":FREQuency:CW {} Hz".format(F))
