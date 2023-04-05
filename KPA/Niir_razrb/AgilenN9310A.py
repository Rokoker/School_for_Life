import time
import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt

class Agilent_GEN(object):
    rm = visa.ResourceManager()
    dev = list(rm.list_resources())
    my_instrument = rm.open_resource("USB0::2391::8216::0115001392::0::INSTR")
    my_instrument.close()


    def check_session(func):


        def _wrapper(self,*args, **kwargs):
            self.my_instrument.open()
            if self.my_instrument.session:
                znach = func(self,*args, **kwargs)
                self.my_instrument.close()


            else:
                print("Error, Agilent N9310A is not aviable")
            return znach
        return _wrapper

    @check_session
    def check_agilent(self):
        _string = self.my_instrument.query("*IDN?")
        print(_string)

    @check_session
    def set_amplitude(self):
        self.my_instrument.write(":AMPLitude:CW -20 dBm")

    @check_session
    def rf_out_stat(self):
        self.my_instrument.write(":RFOutput:STATe ON")

    @check_session
    def mod_stat(self):
        self.my_instrument.write(":MOD:STATe OFF")


