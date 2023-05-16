import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import PyQt5.uic
from main_work import OOP

MainWindow_start, _ = PyQt5.uic.loadUiType("MainWindow_start.ui")
MainWindow_izm, _ = PyQt5.uic.loadUiType("izm.ui")
MainWindow_havenot_connect, _ = PyQt5.uic.loadUiType("havenot_connect.ui")
MainWindow_agilent, _ = PyQt5.uic.loadUiType("window_agilent.ui")

class MessageWindow(QtWidgets.QDialog, MainWindow_havenot_connect):
    def __init__(self, parent=None):
        super(MessageWindow, self).__init__(parent)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна


class MainWindow(QtWidgets.QMainWindow, MainWindow_start):

    def __init__(self):

        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.connect_belan.clicked.connect(self.connect_belan_to_prog)
        self.connect_agilent.clicked.connect(self.connect_agilent_to_prog)
        self.perehod_k_izmereniam.clicked.connect(self.perehod_new_window_izm)

    def perehod_new_window_izm(self):
        if hasattr(oop, "belan"):
            self.window2 = okno_izmerenii(self)
            self.window2.show()
            self.window3 = Window_Agilent(self)
            self.window3.show()
        else:
            message_window = MessageWindow(self)
            message_window.label_2.setText("Спектроанализатор ")
            message_window.label_3.setText("")
            message_window.exec_()

    def connect_belan_to_prog(self):
        if oop.connect_belan():
            self.sost_belan.setText("Подключено")
        else:
            self.sost_belan.setText("Не подключено")

    def connect_agilent_to_prog(self):

        if oop.connect_agilent():
            self.sost_agilent.setText("Подключено")
        else:
            self.sost_agilent.setText("Не подключено")


class okno_izmerenii(QtWidgets.QMainWindow, MainWindow_izm):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.read_data_button.clicked.connect(self.read_data)
        self.inst_har.clicked.connect(self.inst_param)

        self.cent_freq.setText("3000000000")
        self.span.setText("2000000")
        self.filtr_radio.setText("30000")
        self.filtr_video.setText("1000")
        self.razv_Box.setChecked(True)

    def read_data(self):

        result = oop.read_data()
        if result is False:
            window.sost_belan.setText("Не подключено")
            message_window = MessageWindow(self)
            message_window.label_2.setText("Спектроанализатор ")
            message_window.label_3.setText("")
            message_window.exec_()

        else:
            y, x, freq, ampl = result
            self.graph.axes.cla()  # Clear the canvas
            self.graph.axes.plot(x, y)
            self.graph.axes.scatter(freq, ampl, color="red", marker="x")
            self.graph.axes.grid()
            self.graph.draw()
            self.mark_amp.setText("Частота маркера = {}".format(freq))
            self.mark_freq.setText("Амплитуда маркера = {} дБм".format(ampl))
            oop.save_data()

    def inst_param(self):

        cent_freq = int(self.cent_freq.text())
        span_bw = int(self.span.text())
        radio_bw = int(self.filtr_radio.text())
        video_bw = int(self.filtr_video.text())
        razv_check = self.razv_Box.isChecked()
        oop.inst_param(cent_freq, span_bw, radio_bw, video_bw, razv_check)


class Window_Agilent(QtWidgets.QMainWindow, MainWindow_agilent):

    def __init__(self, *args, **kwargs):

        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.gen_freq.setText("3000000000")
        self.gen_ampl.setText("-20")
        self.inst_param.clicked.connect(self.inst_parametrs)
        self.RF_ON.clicked.connect(self.rf_on_off)

    def rf_on_off(self):
        if self.RF_ON.text() == "Включить выход радиочастоты":
            oop.agilent_on_off("ON")
            self.RF_ON.setText("Выключить выход радиочастоты")
        else:
            oop.agilent_on_off("OFF")
            self.RF_ON.setText("Включить выход радиочастоты")

    def inst_parametrs(self):
        freq = int(self.gen_freq.text())
        ampl = int(self.gen_ampl.text())
        oop.inst_param_agilent(freq, ampl)


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    oop = OOP()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение
