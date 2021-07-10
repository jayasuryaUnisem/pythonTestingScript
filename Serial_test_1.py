import serial
import time
import json

ser = serial.Serial("COM7", 115200)
bb = ""
while True:
    cc = ser.readline()
    cc = cc.rstrip().lstrip()
    cc = str(cc, 'utf-8')
    print(cc)
    if(len(cc)>0):
        if(cc[0]=='{'):
            tempJson = json.loads(cc)
            #print("IMEI number: ", tempJson.get("Z1"))
        

