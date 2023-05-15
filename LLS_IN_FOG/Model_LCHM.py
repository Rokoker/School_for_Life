# Импорт бибилиотек
import matplotlib.pyplot as plt
import numpy as np
import pylab
import math
import random
import scipy.fft as sp
from scipy import signal
from scipy.optimize import curve_fit
from statistics import mean
from scipy import special
import scipy.stats as sct
import time



class LLS(object):
    
    #Зададим параметры лазера исходя из условия
    c = 3 * 10**9   # Скорость света


    imp_A = 20       # Амплитуда импульса
    B = 10*10**7          # Скорость возрастания частоты
  
        
    def generator(self):
        izl_sig_A=[]                    # Массив под амплитуды
        
        
        imp_f = 1*10**8     # Начальная частота импульса
        
        self.imp_t = 50 * 10**(-9)      # Длителььность импульса
        
       
        
        self.disc_f = imp_f*500      # Частота дискретизации, пересчитана
                                        # из интервала взятия отсчетов

        self.t_int = 1/self.disc_f   # Интервал взятия отсчетов

                                        
        sig_t=np.arange(0,self.imp_t + self.t_int,self.t_int)  # Временная область для отображения импульса

        
        self.n_sig= len(sig_t)                    # Количество отсчетов для отображения импульса
        
        sig_a_for_SF=[]                           # Массив амплитуд, для дальнейшей свертки в СФ
        amp_imp=[]
        for time in sig_t:
            amp_imp.append(self.imp_A*np.exp(1j*2*np.pi*(imp_f*time+self.B**2/2*time**2)))
            
        self.sig_a_for= amp_imp[:]
        self.N_otch=len(amp_imp)
        return  amp_imp,sig_t,self.sig_a_for                  # Вернули амплитуды сигнала и его временную область



    def canal(self,izl_sig, sig_t,R):                   # Канал без потерь с целью
        t_zad = 2*R/self.c                              # Задержка по веремени в зависимосимости от расстяния R
       
        time_after_target = 2*1000/self.c
        
        for time in range(0, len(sig_t)):
            sig_t[time] =sig_t[time] + t_zad            # Перенесли время сигнала на время приема


               
        do_sig_t=np.arange(0,t_zad,1/self.disc_f)       # Временная область до приема сигнала
       
        do_sig_a=[]                                     # Амплитудная область до приема сигнала

        for time in range(len(do_sig_t)):
            do_sig_a.append(0)                          # Амплитуда на приемнике до приема сигнала равна нулю, заполнили нулями
       
        do_sig_a.extend(izl_sig)                        # Совмещение амплитудных областей до приема сигнала и приема сигнала
        
        do_sig_t = np.append(do_sig_t,sig_t)            # Совмещение временных областей до приема сигнала и приема сигнала

        after_sig_t = np.arange(do_sig_t[-1],time_after_target,1/self.disc_f)       # Временная область после приема сигнала
        after_sig_a = []                                                  # Амплитудная область после приема сигнала

        for time in range(len(after_sig_t)):
            after_sig_a.append(0)                    # Амплитуда на приемнике после приема сигнала равна нулю, заполнили нулями

        do_sig_a.extend(after_sig_a)                 # Совмещение амплитудных областей (до приема, приема сигнала) с областью после приема сигнала
        
        do_sig_t = np.append(do_sig_t,after_sig_t)   # Совмещение временных областей до приема сигнала и приема сигнала

        
        return  do_sig_a, do_sig_t                  # Вернули амплитуды сигнала и его временную область



    def obrabotka(self,sig_a):
        # Найдем отсчет начала приема
        for i in range(len(sig_a)):
            if sig_a[i]>0:
                f_otch=i
                break
        
        N_vse=len(sig_a)
        
        N_start=int(np.floor(f_otch/self.N_otch)*self.N_otch)
        
     

        sig_sf=[]
        for i in range(len(sig_a)):
            sig_sf.append(0)

        for i in range(N_start,N_start+self.N_otch-1):
            
            sig_sf[i]=self.sig_a_for[i-N_start]

        itog=[]
        for i in range(len(sig_a)):
            itog.append((abs(sig_sf[i]+sig_a[i]))**2)
        
        plt.plot(sig_sf)
        plt.show()
        plt.plot(itog)
        plt.show()
   



  

   
        
    def spec(self,y,label, mod = 1):                                 # Функция отображения спектра сигнала

        y=sp.fftshift(sp.fft(y)/len(y))
        frq = sp.fftshift(sp.fftfreq(len(y), d = self.t_int))            # Нормировка оси частот
        # Построение графиков
        plt.figure()
        plt.title(label)
        plt.xlabel("Частота,Гц")
        plt.ylabel("Амплитуда, В")
        plt.plot(frq,np.abs(y.real))
        plt.show()

    def graf(self,y,x,Label):                               # Функция построения графиков временной области
        plt.figure()
        plt.title(Label)
        plt.xlabel("Время,с")
        plt.ylabel("Амплитуда, В")
        plt.plot(x,y)
        plt.draw()


   

for i in range(1):
    r=180

    if __name__ == "__main__":
        print(f"Заданное расстояние {r}")
        kurs = LLS()    
        a_gen, t_gen, sig_a_for_SF = kurs.generator()  # Генерация сигнала
                                                                   
##        kurs.graf(a_gen,t_gen,"Сгенерированный импульс")
##        kurs.spec(a_gen,"Спектр сгенерированного импульса",0)
      
        a_target,t_target = kurs.canal(a_gen,t_gen,r)   # Генерация всей временной шкалы
##        kurs.graf(a_target,t_target,"Принятый сигнал от цели")
##        kurs.spec(a_target,"Спектр принятого сигнал от цели",0)

        kurs.obrabotka(a_target)
     

    
    
    

    

