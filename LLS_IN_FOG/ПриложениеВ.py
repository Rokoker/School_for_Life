#Подключение библиотек
import numpy as np
import matplotlib.pyplot as plt

c=3*10**8                          # Скорость света
imp_lambda= 905*10**-6             # Длина волны импульса
imp_f = c/imp_lambda               # Частота импульса
imp_t = 5*10**-8                   # Длительность импульса
disc_t = imp_t/10                  # Интервал времени взятия отсчетов
disc_f = imp_f*10                      # Частота дискретизации
imp_a=1                            # Амплитуда сигнала
w= 2*np.pi*imp_f                       # Круговая частота импульса
ph0=0                              # Нулевая фаза сигнала
sig=[]                             # Массив под значения импульса
time = np.arange(0,imp_t,1/disc_f) # Временная шкала импульса

# Цикл в котором вы вносим значения сигнала в массив
for t in time:
    sig.append(imp_a)
# Построение графика
plt.plot(time,sig)
plt.show()
