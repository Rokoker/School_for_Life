import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from BelanCK04 import Belan
# from AgilenN9310A importA Agilent_GEN
import numpy as np
import PyQt5.uic

MainWindow_start, _ = PyQt5.uic.loadUiType("MainWindow_start.ui")
MainWindow_izm, _ = PyQt5.uic.loadUiType("izm.ui")
MainWindow_havenot_connect, _ = PyQt5.uic.loadUiType("havenot_connect.ui")


class MessageWindow(QtWidgets.QDialog, MainWindow_havenot_connect):
    def __init__(self,parent=None):
        super(MessageWindow, self).__init__(parent)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна


class MainWindow(QtWidgets.QMainWindow, MainWindow_start):

    def __init__(self):

        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.connect_belan.clicked.connect(self.connect_belan_to_prog)
        self.perehod_k_izmereniam.clicked.connect(self.perehod_new_window_izm)


    def perehod_new_window_izm(self):
        if hasattr(self, "belan"):
            self.window2 = okno_izmerenii(self, belan=self.belan)
            self.window2.show()
        else:
            message_window = MessageWindow(self)
            message_window.label_2.setText("Спектроанализатор ")
            message_window.label_3.setText("")
            message_window.exec_()

    def connect_belan_to_prog(self):
        try:
            if self.belan:
                self.sost_belan.setText("Подключено")
        except AttributeError:
            self.belan = Belan()
            buffer = self.belan.chek_belan()
            if buffer == b'*IDN?;ELVIRA,BELAN CK-4,0000,V 1.0\n':
                self.sost_belan.setText("Подключено")
            else:
                print("Ошибка при подключении спектроанализатора")


class okno_izmerenii(QtWidgets.QMainWindow, MainWindow_izm):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.belan = kwargs.get('belan')
        self.setupUi(self)
        self.ax = self.graph.axes
        self.read_data_button.clicked.connect(self.read_data)

    def read_data(self):
        y = self.belan.read_graf()
        x_start, x_stop, N_otch = self.belan.polosa_x()
        x = np.linspace(x_start, x_stop, N_otch)
        freq, ampl = self.belan.set_marker()
        self.graph.axes.cla()  # Clear the canvas
        self.graph.axes.plot(x, y)
        self.graph.axes.scatter(freq, ampl, color="red", marker="x")
        self.graph.axes.grid()
        self.graph.draw()
        self.mark_amp.setText("Частота маркера = {}".format(freq))
        self.mark_freq.setText("Амплитуда маркера = {} дБм".format(ampl))


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение

'''

if __name__=="__main__":
    belan = Belan()
    belan.chek_belan()
    agilent =Agilent_GEN()
# agilent =Agilent_GEN()
    fff = 3
    agilent.check_agilent()
    agilent.set_amplitude()
    agilent.rf_out_stat()
    agilent.mod_stat()

    agilent.set_freq(fff)
    #belan.set_res()

    #belan.set_span()
    #belan.inst_cent_freq(fff)

    belan.inst_bwid(1)
    belan.set_razv(1)
'''
