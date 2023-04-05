from BelanCK04 import *
from AgilenN9310A import *

if __name__=="__main__":
    belan = Belan()
    agilent =Agilent_GEN()


    agilent.check_agilent()
    agilent.set_amplitude()
    agilent.rf_out_stat()
    agilent.mod_stat()
    belan.chek_belan()
    belan.inst_cent_freq(3)
    belan.inst_bwid(100)
    y = belan.read_graf()
    plt.plot(y)
    plt.grid()
    plt.show()
