# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 19:44:56 2020

@author: Esdra
"""

import serial 

try:
   # bluetooth= serial.Serial('COM5', 9600, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
    bluetooth =  serial.Serial()
    bluetooth.baudrate = 9600
    bluetooth.port = 'COM5'
    bluetooth.timeout = 1
    bluetooth.open()
    bluetooth.write(b'hello') 
    line = bluetooth.readline()
    print(line)
    bluetooth.close()
    

except:
    print("It didn't work very well...")