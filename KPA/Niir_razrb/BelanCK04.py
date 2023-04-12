
import serial
import re
import matplotlib.pyplot as plt
import numpy as np
import time
import re

#Lets go
class Belan(object):
    '''
    Класс анализатора спектра Белан СК4 - Белан 32
    Зададим функции для работы по интерфесу RS-232
    '''

    ser = serial.Serial('/dev/ttyUSB0', 9600, stopbits=2)
    ser.close()

    # Декоратором будем проверять готовность com порта
    def check_com_port(func):

        def _wrapper(self,*args, **kwargs):

            self.ser.open()
            if self.ser.isOpen():
                self.next_razr()
                self.ser.write(b'\n')
                self.ser.readline()
                znach = func(self,*args, **kwargs)
                self.ser.write(b'\n')
                self.ser.readline()
                self.ser.close()
            else:
                print("Error, com port is not aviable")
            return znach
        return _wrapper


    @check_com_port
    def read_graf(self):
        self.ser.write(b':trace:data? trace1;\n')
        self.ser.readline()
        buffer = self.ser.readline()


        buffer = buffer.split()

        otch=[]
        for i in range(len(buffer)):
            buffer[i]=buffer[i].decode('utf-8')
        y_lvl = list(map(float, buffer))

        return y_lvl

    @check_com_port
    def inst_cent_freq(self,freq):
        _string = ':sense:freq:cent {} GHz;'.format(freq)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    @check_com_port
    def inst_bwid(self,bandw):
        _string = ':sense:bwid:res {} kHz;'.format(bandw)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)

    @check_com_port
    def chek_belan(self):
        _string = '*IDN?;'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        buffer = self.ser.readline()
        print(buffer)

    @check_com_port
    def set_razv(self,rej):
        _string = ':INITiate:CONTinuous {};'.format(rej)
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)


    @check_com_port
    def set_marker(self):
        _string = ':trac:math:peak;\n'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        buffer = self.ser.readline()
        buffer = self.ser.readline()
        buffer = buffer.split()
        freq,ampl = list(map(float, buffer))
        print("Частота = {}".format(freq))
        print("Амплитуда = {} дБм".format(ampl))
        return freq,ampl


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
        print(N_otch)
        return x_start,x_stop,N_otch


    @check_com_port
    def set_span(self):
        _string = ':SENSe:FREQ:SPAN 50 kHz;'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)


    @check_com_port
    def set_res(self):
        _string = ':sens:band:res 1 kHz;'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)















##BelCmd(0) = ":sense:freq:cent "            'установка центральной частоты
##BelCmd(1) = ":sense:bwid:res 100Hz;"       'установка полосы пропускания
##BelCmd(2) = ":sense:bwid:vid 100Hz;"       'установка видео полосы пропускания
##BelCmd(3) = ":sense:pow:range " + Replace((CStr(ACH.Oporn_BEL)), ",", ".") + "dBm;" 'установка опорного уровня
##BelCmd(4) = ":sense:pow:rf:att 10;"        'установка аттенюатора
##BelCmd(5) = ":sense:freq:span 2kHz;"       'установка полосы обзора
##BelCmd(7) = ":trace:data? trace1;"         'чтение массива
