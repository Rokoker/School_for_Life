from BelanCK04 import Belan
import numpy as np


class OOP(object):

    def connect(self):
        if hasattr(self, "belan"):
            buffer = self.belan.chek_belan()
            if buffer == b'*IDN?;ELVIRA,BELAN CK-4,0000,V 1.0\n':
                return True
            else:
                return False
        else:
            self.belan = Belan()
            buffer = self.belan.chek_belan()
            if buffer == b'*IDN?;ELVIRA,BELAN CK-4,0000,V 1.0\n':
                return True
            else:
                return False

    def read_data(self):
        if hasattr(self, "belan"):
            y = self.belan.read_graf()
            if y == []:
                return False
            x_start, x_stop, N_otch = self.belan.polosa_x()
            x = np.linspace(x_start, x_stop, N_otch)
            freq, ampl = self.belan.set_marker()

            return y, x, freq, ampl

    def inst_param(self, freq, span_bw, radio_bw, video_bw, razv):

        self.belan.inst_cent_freq(freq)
        self.belan.set_span(span_bw)
        self.belan.set_res(radio_bw)
        self.belan.set_video_filtr(video_bw)
        self.belan.set_razv(razv)

