import serial
import re
import matplotlib.pyplot as plt
import numpy as np
import time
import re
#Скопировал
# Пытаюсь сделать комментарий

class Belan(object):
    '''
    Класс анализатора спектра Белан СК4 - Белан 32
    Зададим функции для работы по интерфесу RS-232
    '''

    ser = serial.Serial('com9', 9600)
    ser.close()
    
    # Декоратором будем проверять готовность com порта
    def check_com_port(func):

        def _wrapper(self,*args, **kwargs):
            
            self.ser.open()
            if self.ser.isOpen():
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
        _string = f':sense:freq:cent {freq} GHz;'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
        
    @check_com_port
    def inst_bwid(self,bandw):
        _string = f':sense:bwid:res 100 kHz;'
        _string = bytes(_string, encoding='utf8')
        self.ser.write(_string)
         
        
    
        

if __name__=="__main__":
    belan = Belan()
    belan.inst_cent_freq(3)
    belan.inst_bwid(100)
    y = belan.read_graf()
    plt.plot(y)
    plt.grid()
    plt.show()
    
##BelCmd(0) = ":sense:freq:cent "            'установка центральной частоты
##BelCmd(1) = ":sense:bwid:res 100Hz;"       'установка полосы пропускания
##BelCmd(2) = ":sense:bwid:vid 100Hz;"       'установка видео полосы пропускания
##BelCmd(3) = ":sense:pow:range " + Replace((CStr(ACH.Oporn_BEL)), ",", ".") + "dBm;" 'установка опорного уровня
##BelCmd(4) = ":sense:pow:rf:att 10;"        'установка аттенюатора
##BelCmd(5) = ":sense:freq:span 2kHz;"       'установка полосы обзора
##BelCmd(7) = ":trace:data? trace1;"         'чтение массива
