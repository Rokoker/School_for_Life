from BelanCK04 import *
from AgilenN9310A import *
import numpy as np

if __name__=="__main__":
    belan = Belan()
    belan.chek_belan()
    agilent =Agilent_GEN()

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
    x_start,x_stop,N_otch = belan.polosa_x()
    freq,ampl = belan.set_marker()
    y = belan.read_graf()
    x = np.linspace(x_start,x_stop,N_otch)
    plt.plot(x, y)
    plt.grid()
    plt.scatter(freq,ampl,color="red",marker ="x")
    plt.show()

