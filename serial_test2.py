# -*- coding: utf-8 -*-
import RPi.GPIO as gpio
import serial
import time
import json
import sys
import os
from datetime import datetime
import paho.mqtt.client as mqtt


broker = "192.168.1.15"  # --> Broker IP address, Here Raspberry is Broker (Note: IP its Dynamic not static)


USB0csvFileName = "USB0_testReport.csv"
USB1csvFileName = "USB1_testReport.csv"
USB2csvFileName = "USB2_testReport.csv"
USB3csvFileName = "USB3_testReport.csv"

txtUSB0FileName = "testReport_USB0.txt"
txtUSB1FileName = "testReport_USB1.txt"
txtUSB2FileName = "testReport_USB2.txt"
txtUSB3FileName = "testReport_USB3.txt"



ts_led = 21
sd_led = 20
imei_led = 16
ssm_led = 12
psm_led = 1
bme_led = 7
lw_led = 8
ws_led = 25
dr_led = 24
st_led = 23
lux_led = 19
reset_button = 2
start_button = 3
ip_start = 6
pass_led = 13

port0 = "USB0"
port1 = "USB1"
port2 = "USB2"
port3 = "USB3"

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(ts_led, gpio.OUT)
gpio.setup(sd_led, gpio.OUT)
gpio.setup(imei_led, gpio.OUT)
gpio.setup(ssm_led, gpio.OUT)
gpio.setup(psm_led, gpio.OUT)
gpio.setup(bme_led, gpio.OUT)
gpio.setup(lw_led, gpio.OUT)
gpio.setup(ws_led, gpio.OUT)
gpio.setup(dr_led, gpio.OUT)
gpio.setup(st_led, gpio.OUT)
gpio.setup(lux_led, gpio.OUT)
gpio.setup(ip_start, gpio.OUT)
gpio.setup(pass_led, gpio.OUT)
gpio.setup(reset_button, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(start_button, gpio.IN, pull_up_down=gpio.PUD_UP)


class buttonState:  #  --> this class used for static variables
    usb0_start = 0
    usb1_start = 0
    usb2_start = 0
    usb3_start = 0

    usb0_stop = 0
    usb1_stop = 0
    usb2_stop = 0
    usb3_stop = 0

    start_all = 0
    stop_all = 0
    clear_screen = 0
    eReset = 0

    flash_test_mode = 0  # --> flash mode 1 and test mode 0

    usb0_flash_start = 0
    usb1_flash_start = 0
    usb2_flash_start = 0
    usb3_flash_start = 0

    usb0_flash_reset = 0
    usb1_flash_reset = 0
    usb2_flash_reset = 0
    usb3_flash_reset = 0

    USB0_sd_status = 0
    USB1_sd_status = 0
    USB2_sd_status = 0
    USB3_sd_status = 0

bs = buttonState()

setP_hw = 3.0
setP_fw = 2.0
setP_at_min = 18.0
setP_at_max = 30.0
setP_ap_min = 80000.0
setP_ap_max = 100000.0
setP_ah_min = 40.0
setP_ah_max = 90.0
setP_lw = 20
setP_rain = 0.2
setP_ws = 0.5
setP_st_min = 20
setP_st_max = 32
setP_psm_min = 5900
setP_psm_max = 8000
setP_ssm_min = 5900
setP_ssm_max = 8000
setP_li = 2
setP_rd = 5


def FileCheck():
    arr = os.listdir('.')
    for i in range(4):
        if "USB"+str(i)+"_testReport.csv" in arr:
            print("File alread Created!!")
        else:
            file = open("USB"+str(i)+"_testReport.csv", "w")
            file.write("Date Time,IMEI,SD Card,HW FW, SW FW,Air Temp,Air Pressure,AIr Humidity,Lead Wetness,Rain,Wind Die,Wind Speed,Soil Temp,P Soil Mois,S Soil Mois,Light Inten, Solar Radi,Remarks\n")
            print("File Created Now")
            file.close()

    try:
        if txtUSB0FileName in arr:
            print("USB0 file alread Created!!")
        else:
            file = open(txtUSB0FileName, "w")
            print("USB0 file created!! Now")
            file.close()

        if txtUSB1FileName in arr:
            print("USB1 file alread Created")
        else:
            file = open(txtUSB1FileName, "w")
            print("USB1 file created now!!")
            file.close()

        if txtUSB2FileName in arr:
            print("USB2 file alread Created")
        else:
            file = open(txtUSB2FileName, "w")
            print("USB2 file created now!!")
            file.close()
        
        if txtUSB3FileName in arr:
            print("USB3 file alread Created")
        else:
            file = open(txtUSB3FileName, "w")
            print("USB3 file created now!!")
            file.close()
    except Exception as err:
        print("USB txt file creating Err: ", err)
        
FileCheck()


def txtWriteValue(payload, port):
    if port == port0:
        file = open(txtUSB0FileName, "a")
        if payload == "Device Powered ON":
            tempPayload = "\n***********************************\n" + DateTime()+"\n"+str(payload)
            file.write(tempPayload+"\n")
        elif payload == "mcu sleep":
            tempPayload = payload + "\n***********************************\n"
            file.write(tempPayload+"\n")
        else:
            file.write(str(payload)+"\n")
        file.close()

    if port == port1:
        file = open(txtUSB1FileName, "a")
        if payload == "Device Powered ON":
            tempPayload = "***********************************\n" + DateTime()+"\n"+str(payload)
            file.write(tempPayload+"\n")
        elif payload == "mcu sleep":
            tempPayload = payload + "\n***********************************\n"
            file.write(tempPayload+"\n")
        else:
            file.write(str(payload)+"\n")
        file.close()

    if port == port2:
        file = open(txtUSB2FileName, "a")
        if payload == "Device Powered ON":
            tempPayload = "***********************************\n" + DateTime()+"\n"+str(payload)
            file.write(tempPayload+"\n")
        elif payload == "mcu sleep":
            tempPayload = payload + "\n***********************************\n" 
            file.write(tempPayload+"\n")
        else:
            file.write(str(payload)+"\n")
        file.close()

    if port == port3:
        file = open(txtUSB3FileName, "a")
        if payload == "Device Powered ON":
            tempPayload = "***********************************\n" + DateTime()+"\n"+str(payload)
            file.write(tempPayload+"\n")
        elif payload == "mcu sleep":
            tempPayload = payload + "\n***********************************\n"
            file.write(tempPayload+"\n")
        else:
            file.write(str(payload)+"\n")
        file.close()


def setPointPub():
    payloadPub(str("sp_hw"), str(setP_hw))
    payloadPub(str("sp_fw"), str(setP_fw))
    payloadPub(str("sp_at_min"), str(setP_at_min))
    payloadPub(str("sp_at_max"), str(setP_at_max))
    payloadPub(str("sp_ap_min"), str(setP_ap_min))
    payloadPub(str("sp_ap_max"), str(setP_ap_max))
    payloadPub(str("sp_ah_min"), str(setP_ah_min))
    payloadPub(str("sp_ah_max"), str(setP_ah_max))
    payloadPub(str("sp_lw"), str(setP_lw))
    payloadPub(str("sp_rain"), str(setP_rain))
    payloadPub(str("sp_ws"), str(setP_ws))
    payloadPub(str("sp_st_min"), str(setP_st_min))
    payloadPub(str("sp_st_max"), str(setP_st_max))
    payloadPub(str("sp_psm_min"), str(setP_psm_min))
    payloadPub(str("sp_psm_max"), str(setP_psm_max))
    payloadPub(str("sp_ssm_min"), str(setP_ssm_min))
    payloadPub(str("sp_ssm_max"), str(setP_ssm_max))
    payloadPub(str("sp_li"), str(setP_li))
    payloadPub(str("sp_rd"), str(setP_rd))


serMain = [0 for i in range(4)]

# for checking the Serial COM ports (0 to 3) // (note: Linux <$ ls /dev/tty*> for check the COM Ports )
for i in range(4):
    try:
        serMain[i] = serial.Serial("/dev/ttyUSB"+str(i), 115200)
    except:
        serMain[i] = "ERR"

# restart_program --> software Reset
def restart_program():  
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    # Print result of connection attempt
    print("Connected with result code Update_081321 {0}".format(str(rc)))
    client.subscribe("button") 

def on_message(client, userdata, message):
    tempPayload = str(message.payload.decode("utf-8"))
    print("Payload: ", tempPayload)

    if tempPayload == "USB0_stop":
        bs.usb0_start = 0
        portClear("USB0")
    if tempPayload == "USB1_stop":
        bs.usb1_start = 0
        portClear("USB1")
    if tempPayload == "USB2_stop":
        bs.usb2_start = 0
        portClear("USB2")
    if tempPayload == "USB3_stop":
        bs.usb3_start = 0
        portClear("USB3")

    if tempPayload == "USB0_start":
        if serMain[0] != "ERR":
            serMain[0].close()
            time.sleep(0.2)
            serMain[0].open()
            time.sleep(1)
            bs.usb0_start = 1
    if tempPayload == "USB1_start":
        if serMain[1] != "ERR":
            serMain[1].close()
            time.sleep(0.2)
            serMain[1].open()
            bs.usb1_start = 1
    if tempPayload == "USB2_start":
        if serMain[2] != "ERR":
            serMain[2].close()
            time.sleep(0.2)
            serMain[2].open()
            bs.usb2_start = 1
    if tempPayload == "USB3_start":
        if serMain[3] != "ERR":
            serMain[3].close()
            time.sleep(0.2)
            serMain[3].open()
            bs.usb3_start = 1

    if tempPayload == "startAll":
        if serMain[0] != "ERR":
            serMain[0].close()
            time.sleep(0.2)
            serMain[0].open()
            time.sleep(1)
            bs.usb0_start = 1
        if serMain[1] != "ERR":
            serMain[1].close()
            time.sleep(0.2)
            serMain[1].open()
            time.sleep(1)
            bs.usb1_start = 1
        if serMain[2] != "ERR":
            serMain[2].close()
            time.sleep(0.2)
            serMain[2].open()
            time.sleep(1)
            bs.usb2_start = 1
        if serMain[3] != "ERR":
            serMain[3].close()
            time.sleep(0.2)
            serMain[3].open()
            time.sleep(1)
            bs.usb3_start = 1

    if tempPayload == "stopAll":
        bs.usb0_start = 0
        bs.usb1_start = 0
        bs.usb2_start = 0
        bs.usb3_start = 0
        portClear("USB0")
        portClear("USB1")
        portClear("USB2")
        portClear("USB3")
        
    if tempPayload == "eReset":
        print("Software Reset!!")
        time.sleep(1)
        restart_program()

    if tempPayload == "clearScreen":
        dashoboardClear(0)
    
    if tempPayload == "flash_mode":
        bs.flash_test_mode = 1
    if tempPayload == "test_mode":
        bs.flash_test_mode = 0
    
    if tempPayload == port0+"_flash_start":
        if bs.flash_test_mode == 1:
            bs.usb0_flash_start = 1
    if tempPayload == port1+"_flash_start":
        if bs.flash_test_mode == 1:
            bs.usb1_flash_start = 1
    if tempPayload == port2+"_flash_start":
        if bs.flash_test_mode == 1:
            bs.usb2_flash_start = 1
    if tempPayload == port3+"_flash_start":
        if bs.flash_test_mode == 1:
            bs.usb3_flash_start = 1
    
    if tempPayload == port0+"_flash_reset":
        if bs.flash_test_mode == 1:
            bs.usb0_flash_reset = 1
    if tempPayload == port1+"_flash_reset":
        if bs.flash_test_mode == 1:
            bs.usb1_flash_reset = 1
    if tempPayload == port2+"_flash_reset":
        if bs.flash_test_mode == 1:
            bs.usb2_flash_reset = 1
    if tempPayload == port3+"_flash_reset":
        if bs.flash_test_mode == 1:
            bs.usb3_flash_reset = 1



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker)
client.loop_start()
time.sleep(2)

# DateTime --> Returns the system datetime: (DD/MM/YY hh:mm:ss)
def DateTime():
    now = datetime.now()
    now = str(now.strftime("%d/%m/%y %H:%M:%S"))
    return now

# payloadPub --> publiching the data packet without packet loss    
def payloadPub(topic, payload):
    pubCheck = client.publish(topic, payload)
    while pubCheck[0] != 0:
        pubCheck = client.publish(topic, payload)
        time.sleep(0.1) 


def checkValue(imei, hw_ver, firm_ver, air_temp, air_p, air_humidity, leaf_wetness, rain, wind_dir, wind_speed, soil_temp, p_soil_mois, s_soil_mois, light_inten, solar_radi, port):
    tempSDstatus = eval("bs."+port+"_sd_status")
    print("***********************************")
    if(len(imei) == 15):
        print("IMEI Done")
        payloadPub("imei", str(imei))
        payloadPub(port+"_IMEI_led", "OK")
    else:
        print("IMEI Failed")
        payloadPub("imei", str("IMEI Failed"))
        payloadPub(port+"_IMEI_led", "ERR")

    if((air_temp > setP_at_min and air_temp < setP_ah_max) and (air_p > setP_ap_min and air_p < setP_ap_max) and (air_humidity > setP_ah_min and air_humidity < setP_ah_max)):
        print("BME Sensor Test Done")
        payloadPub("at", str(air_temp))
        payloadPub("ap", str(air_p))
        payloadPub("ah", str(air_humidity))
        payloadPub(port+"_BME_led", "OK")
    else:
        print("BME Sensor Test Failed")
        payloadPub("at", str(air_temp)+" : Failed")
        payloadPub("ap", str(air_p)+" : Failed")
        payloadPub("ah", str(air_humidity)+" : Failed")
        payloadPub(port+"_BME_led", "ERR")

    if(leaf_wetness > setP_lw):
        print("Leaf Wetness Done")
        payloadPub("lw", str(leaf_wetness))
        payloadPub(port+"_LW_led", "OK")
    else:
        print("Leaf Wetness Failed")
        payloadPub("lw", str(leaf_wetness)+" : Failed")
        payloadPub(port+"_LW_led", "ERR")

    if((rain > setP_rain) and (len(wind_dir) > 0)):
        print("Rain Sensor and Wind Direction Test Done")
        payloadPub("rc", str(rain))
        payloadPub("wd", str(wind_dir))
        payloadPub(port+"_DC_led", "OK")
    else:
        print("Rain Sensor and Wind Direction Test Failed")
        payloadPub("rc", str(rain)+" : Failed")
        payloadPub("wd", str(wind_dir)+" : Failed")
        payloadPub(port+"_DC_led", "ERR")

    if(wind_speed > setP_ws):
        print("Wind Speed Done")
        payloadPub("ws", str(wind_speed))
        payloadPub(port+"_WS_led", "OK")
    else:
        print("Wind Speed Failed")
        payloadPub("ws", str(wind_speed)+" : Failed")
        payloadPub(port+"_WS_led", "ERR")

    if(soil_temp > setP_st_min and soil_temp < setP_st_max):
        print("Soil Temperature Test Done")
        payloadPub("st", str(soil_temp))
        payloadPub(port+"_ST_led", "OK")
    else:
        print("Soil Temperature Test Failed")
        payloadPub("st", str(soil_temp)+" : Failed")
        payloadPub(port+"_ST_led", "ERR")

    if(p_soil_mois > setP_psm_min and p_soil_mois < setP_psm_max):
        print("Primery Soil Mositure Sensor Test Done")
        payloadPub("psm", str(p_soil_mois))
        payloadPub(port+"_PSM_led", "OK")
    else:
        print("Primery Soil Mositure Sensor Test Failed")
        payloadPub("psm", str(p_soil_mois)+" : Failed")
        payloadPub(port+"_PSM_led", "ERR")

    if(s_soil_mois > setP_ssm_min and s_soil_mois < setP_ssm_max):
        print("Secondary Soil Mositure Sensor Test Done")
        payloadPub("ssm", str(s_soil_mois))
        payloadPub(port+"_SSM_led", "OK")
    else:
        print("Secondary Soil Mositure Sensor Test Failed")
        payloadPub("ssm", str(s_soil_mois)+" : Failed")
        payloadPub(port+"_SSM_led", "ERR")

    if((light_inten > setP_li) and (solar_radi > setP_rd)):
        print("Lux Sensor Test Done")
        payloadPub("li", str(light_inten))
        payloadPub("sr", str(solar_radi))
        payloadPub(port+"_LUX_led", "OK")
    else:
        print("Lux Sensor Test Failed")
        payloadPub("li", str(light_inten)+" : Failed")
        payloadPub("sr", str(solar_radi)+" : Failed")
        payloadPub(port+"_LUX_led", "ERR")
    
    file = open(port+"_testReport.csv", "a")
    file.write(str(DateTime())+","+str(imei)+","+str(tempSDstatus)+","+str(hw_ver)+","+str(firm_ver)+","+str(air_temp)+","+str(air_p)+","+str(air_humidity)+","+str(leaf_wetness)+","+str(rain)+","+str(wind_dir)+","+str(wind_speed)+","+str(soil_temp)+","+str(p_soil_mois)+","+str(s_soil_mois)+","+str(light_inten)+","+str(solar_radi)+"\n")
    time.sleep(0.01)
    file.close()
    exec("bs."+port+"_sd_status=0")
    print("***********************************")


#functionCheck --> Payload Handling and compare
def functionCheck(payload, port):
    payloadPub(port, payload)

    if payload == "Device Powered ON":
        print("Device ON Done")
        payloadPub(port+"_DS_led", "OK")
    
    elif payload == "<<< MSG: SD card initialization Successful! >>>":
        print("SD Card Done")
        payloadPub(port+"_SD_led", "OK")
        exec("bs."+port+"_sd_status='OK'")
    
    elif payload == "<<< WARNING: SD card initialization failed / Not Detected! >>>":
        print("SD not Detected")
        payloadPub(port+"_SD_led", "ERR")
        exec("bs."+port+"_sd_status='ERR'")
    
    elif payload == "mcu sleep":
        print("\n***********************************")
        print("Sleep Mode")
        print("***********************************")
        if port == "USB0":
            bs.usb0_start = 0
        if port == "USB1":
            bs.usb1_start = 0
        if port == "USB2":
            bs.usb2_start = 0
        if port == "USB3":
            bs.usb3_start = 0
    try:
        if(payload[0] == '{'):  # JSON fromat starts from {
            tempJson = json.loads(payload)
            imei = tempJson.get("Z1")
            imeiF = str(imei.encode("utf-8"))
            hw_ver = float(tempJson.get("Z4"))
            firm_ver = float(tempJson.get("Z8"))
            air_temp = float(tempJson["Z5"]["A"])
            air_pressure = float(tempJson["Z5"]["B"])
            air_humidity = float(tempJson["Z5"]["C"])
            leaf_wetness = int(tempJson["Z5"]["D"])
            rain = float(tempJson["Z5"]["G"])
            wind_dir = tempJson["Z5"]["F"]
            wind_dir = str(wind_dir.encode("utf-8"))
            wind_speed = float(tempJson["Z5"]["E"])
            soil_temp = float(tempJson["Z5"]["H"])
            p_soil_mois = int(tempJson["Z5"]["I"])
            s_soil_mois = int(tempJson["Z5"]["J"])
            light_int = tempJson["Z5"]["O"]
            solar_radi = tempJson["Z5"]["P"]
            #print("IMEI number: ", tempJson.get("Z1"))
            print("***********************************")
            print("IMEI: ", imeiF)
            print("Hardware Version: ", hw_ver)
            print("firmware Version: ", firm_ver)
            print("Air Temperature: ", air_temp)
            print("Air Pressure: ", air_pressure)
            print("Air Humidity: ", air_humidity)
            print("Leaf Wetness: ", leaf_wetness)
            print("Rain in mm: ", rain)
            print("Wind Direction: ", wind_dir)
            print("Wind Speed: ", wind_speed)
            print("Soil Temperature: ", soil_temp)
            print("Primary Soil Mositure: ", p_soil_mois)
            print("Secondary Soil Moisture: ", s_soil_mois)
            print("Light Intensity: ", light_int)
            print("Solar Radiation: ", solar_radi)
            print("***********************************")                               
            checkValue(imeiF, hw_ver, firm_ver, air_temp, air_pressure, air_humidity, leaf_wetness,
            rain, wind_dir, wind_speed, soil_temp, p_soil_mois, s_soil_mois, light_int, solar_radi, port)               
    except Exception as err:
        print("Error: ", err)
        payloadPub(port, str(err))     
          
    try:
        if(payload.index("Up-time:")):
            res = [int(i) for i in payload.split() if i.isdigit()]
            payloadPub("uptimeValue", str(res))
            if res[0] > 3 and res[0]<6:
                payloadPub(port+"_DUPT_led", "OK")
            else:
                payloadPub(port+"_DUPT_led", "ERR")
    except:
        tempTry = 0
        
def dashoboardClear(portClear):
    for i in range(4):
        payloadPub("USB"+str(i), "")
        payloadPub("USB"+str(i)+"_DS_led", "WT")
        payloadPub("USB"+str(i)+"_SD_led", "WT")
        payloadPub("USB"+str(i)+"_DUPT_led", "WT")
        payloadPub("USB"+str(i)+"_IMEI_led", "WT")
        payloadPub("USB"+str(i)+"_BME_led", "WT")
        payloadPub("USB"+str(i)+"_LW_led", "WT")
        payloadPub("USB"+str(i)+"_PSM_led", "WT")
        payloadPub("USB"+str(i)+"_SSM_led", "WT")
        payloadPub("USB"+str(i)+"_ST_led", "WT")
        payloadPub("USB"+str(i)+"_WS_led", "WT")
        payloadPub("USB"+str(i)+"_DC_led", "WT")
        payloadPub("USB"+str(i)+"_LUX_led", "WT")
        payloadPub("USB"+str(i)+"_FM_led", "WT")
        payloadPub("USB"+str(i)+"_TM_led", "WT") 
        payloadPub("USB"+str(i)+"_flash_status", "WT")
        if portClear==1:
            payloadPub("USB"+str(i)+"_Status", "WT")


def portClear(port):
    payloadPub(port+"_DS_led", "WT")
    payloadPub(port+"_SD_led", "WT")
    payloadPub(port+"_DUPT_led", "WT")
    payloadPub(port+"_IMEI_led", "WT")
    payloadPub(port+"_BME_led", "WT")
    payloadPub(port+"_LW_led", "WT")
    payloadPub(port+"_PSM_led", "WT")
    payloadPub(port+"_SSM_led", "WT")
    payloadPub(port+"_ST_led", "WT")
    payloadPub(port+"_WS_led", "WT")
    payloadPub(port+"_DC_led", "WT")
    payloadPub(port+"_LUX_led", "WT")
    payloadPub(port, "")
    

def portCheck():
    for i in range(4):
        if serMain[i] != "ERR":
            payloadPub("USB"+str(i)+"_Status", "OK")
        else:
            payloadPub("USB"+str(i)+"_Status", "ERR")
            

def flashing(port):
    print("Flashing Start @ Port: ", port)
    payloadPub(port, "Flashing Start")
    payloadPub(port+"_flash_status", "ST")
    binPath = "stm32loader -p /dev/tty"+port+" -e -w -v fasal-3p0-SensorTest-RevC-29June2021-v1p7.bin"
    flashing_status = os.system(binPath)
    if flashing_status == 0:
        return True
    else:
        return False

dashoboardClear(1)

time.sleep(1)

portCheck()

while True:
    if bs.flash_test_mode == 0:
        payloadPub(port0+"_FM_led", "ERR")
        payloadPub(port1+"_FM_led", "ERR")
        payloadPub(port2+"_FM_led", "ERR")
        payloadPub(port3+"_FM_led", "ERR")

        payloadPub(port0+"_TM_led", "OK")
        payloadPub(port1+"_TM_led", "OK")
        payloadPub(port2+"_TM_led", "OK")
        payloadPub(port3+"_TM_led", "OK")
        if serMain[0] != "ERR" and bs.usb0_start == 1:
            payloadPub("USB0_TS_led", "OK")
            ser = serMain[0]
            check = ser.in_waiting
            if check>0:
                cc = ser.readline().rstrip('\r\n').lstrip()
                if len(cc)>0:
                    print("USB0: ", cc)
                    txtWriteValue(cc, port0)
                    functionCheck(cc, "USB0")
        else:
            payloadPub("USB0_TS_led", "ERR")

        if serMain[1] != "ERR" and bs.usb1_start == 1 and bs.flash_test_mode == 0:
            payloadPub("USB1_TS_led", "OK")
            ser = serMain[1]
            check = ser.in_waiting
            if check>0:
                cc = ser.readline().rstrip('\r\n').lstrip()
                if len(cc)>0:
                    print("USB1: ", cc)
                    txtWriteValue(cc, port1)
                    functionCheck(cc, "USB1")
        else:
            payloadPub("USB1_TS_led", "ERR")
        
        if serMain[2] != "ERR" and bs.usb2_start == 1 and bs.flash_test_mode == 0:
            payloadPub("USB2_TS_led", "OK")
            ser = serMain[2]
            check = ser.in_waiting
            if check>0:
                cc = ser.readline().rstrip('\r\n').lstrip()
                if len(cc)>0:
                    print("USB2: ", cc)
                    txtWriteValue(cc, port2)
                    functionCheck(cc, "USB2")
        else:
            payloadPub("USB2_TS_led", "ERR")

        if serMain[3] != "ERR" and bs.usb3_start == 1 and bs.flash_test_mode == 0:
            payloadPub("USB3_TS_led", "OK")
            ser = serMain[3]
            check = ser.in_waiting
            if check>0:
                cc = ser.readline().rstrip('\r\n').lstrip()
                if len(cc)>0:
                    print("USB3: ", cc)
                    txtWriteValue(cc, port3)
                    functionCheck(cc, "USB3")
        else:
            payloadPub("USB3_TS_led", "ERR")

    elif bs.flash_test_mode == 1:
        payloadPub(port0+"_FM_led", "OK")
        payloadPub(port1+"_FM_led", "OK")
        payloadPub(port2+"_FM_led", "OK")
        payloadPub(port3+"_FM_led", "OK")

        payloadPub(port0+"_TM_led", "ERR")
        payloadPub(port1+"_TM_led", "ERR")
        payloadPub(port2+"_TM_led", "ERR")
        payloadPub(port3+"_TM_led", "ERR")
        while bs.flash_test_mode == 1:
            if bs.usb0_flash_start == 1:
                result = flashing(port0)
                if result == True:
                    print(port0,": Flashing and Verification Done")
                    payloadPub(port0, "Flashing and Verification Done")
                    payloadPub(port0+"_flash_status", "OK")
                    while bs.usb0_flash_reset == 0:
                        time.sleep(0.6)
                    time.sleep(1)
                    payloadPub(port0+"_flash_status", "WT")
                    payloadPub(port0, "")
                    bs.usb0_flash_reset = 0
                    bs.usb0_flash_start = 0
                else:
                    print(port0, ": Flashing Error, Check Power and Button State")
                    payloadPub(port0, "Flashing Err, ck pwr & Btn State")
                    payloadPub(port0+"_flash_status", "ERR")
                    while bs.usb0_flash_reset == 0:
                        time.sleep(0.6)
                    time.sleep(1)
                    payloadPub(port0+"_flash_status", "WT")
                    payloadPub(port0, "")
                    bs.usb0_flash_reset = 0
                    bs.usb0_flash_start = 0
            
            if bs.usb1_flash_start == 1:
                result = flashing(port1)
                if result == True:
                    print(port1,": Flashing and Verification Done")
                    payloadPub(port1, "Flashing and Verification Done")
                    payloadPub(port1+"_flash_status", "OK")
                    while bs.usb1_flash_reset == 0:
                        time.sleep(0.6)
                    time.sleep(1)
                    payloadPub(port1+"_flash_status", "WT")
                    payloadPub(port0, "")
                    bs.usb1_flash_reset = 0
                    bs.usb1_flash_start = 0
                else:
                    print(port1, ": Flashing Error, Check Power and Button State")
                    payloadPub(port1, "Flashing Err, ck pwr & Btn State")
                    payloadPub(port1+"_flash_status", "ERR")
                    while bs.usb1_flash_reset == 0:
                        time.sleep(0.6)
                    time.sleep(1)
                    payloadPub(port1+"_flash_status", "WT")
                    payloadPub(port0, "")
                    bs.usb1_flash_reset = 0
                    bs.usb1_flash_start = 0
            
            if bs.usb2_flash_start == 1:
                result = flashing(port2)
                if result == True:
                    print(port2,": Flashing and Verification Done")
                    payloadPub(port2, "Flashing and Verification Done")
                    payloadPub(port2+"_flash_status", "OK")
                    while bs.usb2_flash_reset == 0:
                        time.sleep(0.6)
                    time.sleep(1)
                    payloadPub(port2+"_flash_status", "WT")
                    payloadPub(port2, "")
                    bs.usb2_flash_reset = 0
                    bs.usb2_flash_start = 0
                else:
                    print(port2, ": Flashing Error, Check Power and Button State")
                    payloadPub(port2, "Flashing Err, ck pwr & Btn State")
                    payloadPub(port2+"_flash_status", "ERR")
                    while bs.usb2_flash_reset == 0:
                        time.sleep(0.6)
                    time.sleep(1)
                    payloadPub(port2+"_flash_status", "WT")
                    payloadPub(port2, "")
                    bs.usb2_flash_reset = 0
                    bs.usb2_flash_start = 0
            
            if bs.usb3_flash_start == 1:
                result = flashing(port3)
                if result == True:
                    print(port3,": Flashing and Verification Done")
                    payloadPub(port3, "Flashing and Verification Done")
                    payloadPub(port3+"_flash_status", "OK")
                    while bs.usb3_flash_reset == 0:
                        time.sleep(0.6)
                    time.sleep(1)
                    payloadPub(port3+"_flash_status", "WT")
                    payloadPub(port3, "")
                    bs.usb3_flash_reset = 0
                    bs.usb3_flash_start = 0
                else:
                    print(port3, ": Flashing Error, Check Power and Button State")
                    payloadPub(port3, "Flashing Err, ck pwr & Btn State")
                    payloadPub(port3+"_flash_status", "ERR")
                    while bs.usb3_flash_reset == 0:
                        time.sleep(0.6)
                    time.sleep(1)
                    payloadPub(port3+"_flash_status", "WT")
                    payloadPub(port3, "")
                    bs.usb3_flash_reset = 0
                    bs.usb3_flash_start = 0

    time.sleep(0.1) 
    



