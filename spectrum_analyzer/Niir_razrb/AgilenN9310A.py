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


