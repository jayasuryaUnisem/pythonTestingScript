import serial
import time
import json

ser = serial.Serial("/dev/ttyUSB0", 115200)
bb = ""
while True:
    cc = ser.readline()

   # cc = cc.rstrip().lstrip()
   # cc = str(cc, 'utf-8')
    cc = cc.rstrip('\r\n').lstrip()
    print(cc)
    



