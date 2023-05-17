from BelanCK04 import Belan
from AgilenN9310A import Agilent
import numpy as np
import csv
import datetime

# Класс для удобно взаимодествия с приборами
# Его можно подгружать как в сервер так и в GUI


class OOP(object):

    # Подключение и проверка спектроанализатора
    def connect_belan(self):
        if hasattr(self, "belan"):  # Если уже подключался - просто проверка
            buffer = self.belan.chek_belan()  # Возвращает свое название
            if buffer == b'*IDN?;ELVIRA,BELAN CK-4,0000,V 1.0\n':
                return True
            else:
                return False
        else:
            self.belan = Belan()  # Если еще не подключался - создание атрибута
            buffer = self.belan.chek_belan()
            if buffer == b'*IDN?;ELVIRA,BELAN CK-4,0000,V 1.0\n':
                return True
            else:
                return False

    # Чтение графика
    def read_data(self):
        if hasattr(self, "belan"):
            y = self.belan.read_graf()
            if y == [] or y is False:  # Проверка, иногда может вернуть пустой массив
                return False
            x_start, x_stop, N_otch = self.belan.polosa_x()  # Получение контрольных точек оси Х
            x = np.linspace(x_start, x_stop, N_otch)  # Генерация оси X
            freq, ampl = self.belan.set_marker()  # Получение координат маркера

            return y, x, freq, ampl

    # Установка параметров спектроанализатора
    def inst_param(self, freq, span_bw, radio_bw, video_bw, razv):

        self.belan.set_razv(razv)
        self.belan.inst_cent_freq(freq)
        self.belan.set_span(span_bw)
        self.belan.set_res(radio_bw)
        self.belan.set_video_filtr(video_bw)

    # Подключение генератора, все по аналогии
    def connect_agilent(self):
        if hasattr(self, "agilent"):
            buffer = self.agilent.check_agilent()
            if buffer == "Agilent Technologies,N9310A,CN0115001392,A-02-04  ":
                self.agilent_on_off("OFF")
                self.agilent.mod_stat()  # Выключение модуляции
                return True
            else:
                return False
        else:
            self.agilent = Agilent()
            buffer = self.agilent.check_agilent()
            if buffer == 'Agilent Technologies,N9310A,CN0115001392,A-02-04  ':
                self.agilent_on_off("OFF")
                self.agilent.mod_stat()
                return True
            else:
                return False

    # Управление выходом радиочастоты генератора
    def agilent_on_off(self, ON_OFF):
        self.agilent.rf_out_stat(ON_OFF)

    # Установка параметров генератора
    def inst_param_agilent(self, freq, ampl):
        self.agilent.set_freq(freq)
        self.agilent.set_amplitude(ampl)

    # Сохранение данных
    def save_data(self):
        now = datetime.datetime.now()
        result = self.read_data()
        if result is False:
            pass  # Надо обработать ошибку
        else:
            # Распаковка и запись
            y, x, freq, ampl = result
            with open('coords.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['time, ', now.strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow(['x', 'y'])
                for i in range(len(x)):
                    writer.writerow([x[i], y[i]])
