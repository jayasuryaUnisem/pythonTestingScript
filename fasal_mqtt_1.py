import RPi.GPIO as gpio
import serial
import time
import json
import os
from datetime import datetime
import paho.mqtt.client as paho

fname_static = "tReportStatic.csv"
broker = "192.168.1.15"

def on_message(client, userdata, message):
    time.sleep(1)
    print("Payload: ", str(message.payload.decode("utf-8")))

client = paho.Client("client-001")
client.on_message = on_message
client.connect(broker)
client.loop_start()
client.publish("test","check1")
time.sleep(4)


gpio.cleanup()
try:
    arr = os.listdir(os.getcwd())
    print(arr)
    if fname_static in arr:
        print("File Already Exist!!")
    else:
        file = open(fname_static, "a")
        file.write("DateTime,IMEI,SD Card,HW Ver,Firm Ver,Air Temp,Air Pressure,AIr Humidity,Lead Wetness,Rain,Wind Die,Wind Speed,Soil Temp,P Soil Mois,S Soil Mois,Light Inten, Solar Radi,Remarks\n")
        file.close()
except Exception as err:
    arr = os.listdir()
    print(arr)
    print("File in not created!!")
    print("Error: ", err)


def DateTime():
    now = datetime.now()
    now = str(now.strftime("%d/%m%y %H:%M:%S"))
    return now

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

#Serial Communication configs
try:
    ser = serial.Serial("/dev/ttyUSB0", 115200)
except:
    gpio.cleanup()
    while 1:
        print("Serial Port Not connected !")
        time.sleep(1)
###gpio.cleanup()

#Defined or Default Setpoint for compare the sensor values
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


def setPointPub():
    payloadPub(str("sp_hw", str(setP_hw)))
    payloadPub(str("sp_fw", str(setP_fw)))
    payloadPub(str("sp_at_min", str(setP_at_min)))
    payloadPub(str("sp_at_max", str(setP_at_max)))
    payloadPub(str("sp_ap_min", str(setP_ap_min)))
    payloadPub(str("sp_ap_max", str(setP_ap_max)))
    payloadPub(str("sp_ah_min", str(setP_ah_min)))
    payloadPub(str("sp_ah_max", str(setP_ah_max)))
    payloadPub(str("sp_lw", str(setP_lw)))
    payloadPub(str("sp_rain", str(setP_rain)))
    payloadPub(str("sp_ws", str(setP_ws)))
    payloadPub(str("sp_st_min", str(setP_st_min)))
    payloadPub(str("sp_st_max", str(setP_st_max)))
    payloadPub(str("sp_psm_min", str(setP_psm_min)))
    payloadPub(str("sp_psm_max", str(setP_psm_max)))
    payloadPub(str("sp_ssm_min", str(setP_ssm_min)))
    payloadPub(str("sp_ssm_max", str(setP_ssm_max)))
    payloadPub(str("sp_li", str(setP_li)))
    payloadPub(str("sp_rd", str(setP_rd)))




def csvWrite(imei, hw_ver, firm_ver, air_temp, air_p, air_hum, lw, rain, wDir, wSpeed, soil_temp, psm, ssm, light_int, s_radi):
    try:
        file = open(fname_static, "a")
        payload = str(DateTime())+","+str(imei)+","+"OK,"+str(hw_ver)+","+str(firm_ver)+","+str(air_temp)+","+str(air_p)+","+str(air_hum)+","+str(lw)+","+str(rain)+","+str(wDir)+","+str(wSpeed)+","+str(soil_temp)+","+str(psm)+","+str(ssm)+","+str(light_int)+","+str(solar_radi)+",PASS"
        file.write(payload+"\n")
        print("File Write Successful")
        file.close()
    except Exception as err:
        print("File Write Error")
        print(err)
#Fuction for sensor value test and indication
def check(imei, hw_ver, firm_ver, air_temp, air_p, air_humidity, leaf_wetness, rain, wind_dir, wind_speed, soil_temp, p_soil_mois, s_soil_mois, light_inten, solar_radi):
    print("***********************************")
    if(len(imei)==15):
        print("IMEI Done")
        gpio.output(imei_led, gpio.HIGH)
        payloadPub("imei",str(imei))
    else:
        print("IMEI Failed")
        gpio.output(imei_led, gpio.LOW)
        payloadPub("imei",str("IMEI Failed"))

    if(hw_ver==setP_hw):
        print("Hardware Version Done")
        payloadPub("Hardware Version",str(hw_ver))
    else:
        print("Hardware Version Failed")
        payloadPub("Hardware Version",str(hw_ver)+": Version Failed")

    if(firm_ver==setP_fw):
        print("Firmware Version Done")
        payloadPub("Firmware Version",str(firm_ver))
    else:
        print("Firmware Version Failed")
        payloadPub("Firmware Version",str(firm_ver)+": Firmware Failed")

    if((air_temp > setP_at_min and air_temp < setP_ah_max) and (air_p > setP_ap_min and air_p < setP_ap_max) and (air_humidity > setP_ah_min and air_humidity < setP_ah_max)):
        print("BME Sensor Test Done")
        gpio.output(bme_led, gpio.HIGH)
        payloadPub("at",str(air_temp))
        payloadPub("ap",str(air_pressure))
        payloadPub("ah",str(air_humidity))
    else:
        print("BME Sensor Test Failed")
        gpio.output(bme_led, gpio.LOW)
        payloadPub("at",str(air_temp)+" : Failed")
        payloadPub("ap",str(air_pressure)+" : Failed")
        payloadPub("ah",str(air_humidity)+" : Failed")

    if(leaf_wetness > setP_lw):
        print("Leaf Wetness Done")
        gpio.output(lw_led, gpio.HIGH)
        payloadPub("lw",str(leaf_wetness))
    else:
        print("Leaf Wetness Failed")
        gpio.output(lw_led, gpio.LOW)
        payloadPub("lw",str(leaf_wetness)+" : Failed")

    if((rain > setP_rain) and (len(wind_dir)>0)):
        print("Rain Sensor and Wind Direction Test Done")
        gpio.output(dr_led, gpio.HIGH)
        payloadPub("rc",str(rain))
        payloadPub("wd",str(wind_dir))
    else:
        print("Rain Sensor and Wind Direction Test Failed")
        gpio.output(dr_led, gpio.LOW)
        payloadPub("rc",str(rain)+" : Failed")
        payloadPub("wd",str(wind_dir)+" : Failed")

    if(wind_speed > setP_ws):
        print("Wind Speed Done")
        gpio.output(ws_led, gpio.HIGH)
        payloadPub("ws",str(wind_speed))
    else:
        print("Wind Speed Failed")
        gpio.output(ws_led, gpio.LOW)
        payloadPub("ws",str(wind_speed)+" : Failed")

    if(soil_temp > setP_st_min and soil_temp < setP_st_max):
        print("Soil Temperature Test Done")
        gpio.output(st_led, gpio.HIGH)
        payloadPub("st",str(soil_temp))
    else:
        print("Soil Temperature Test Failed")
        gpio.output(st_led, gpio.LOW)
        payloadPub("st",str(soil_temp)+" : Failed")

    if(p_soil_mois > setP_psm_min and p_soil_mois < setP_psm_max):
        print("Primery Soil Mositure Sensor Test Done")
        gpio.output(psm_led, gpio.HIGH)
        payloadPub("psm",str(p_soil_mois))
    else:
        print("Primery Soil Mositure Sensor Test Failed")
        gpio.output(psm_led, gpio.LOW)
        payloadPub("psm",str(p_soil_mois)+" : Failed")

    if(s_soil_mois > setP_ssm_min and s_soil_mois < setP_ssm_max):
        print("Secondary Soil Mositure Sensor Test Done")
        gpio.output(ssm_led, gpio.HIGH)
        payloadPub("ssm",str(s_soil_mois))
    else:
        print("Secondary Soil Mositure Sensor Test Failed")
        gpio.output(ssm_led, gpio.LOW)
        payloadPub("ssm",str(s_soil_mois)+" : Failed")

    if((light_inten > setP_li) and (solar_radi > setP_rd)):
        print("Lux Sensor Test Done")
        gpio.output(lux_led, gpio.HIGH)
        payloadPub("li",str(light_inten))
        payloadPub("sr",str(solar_radi))
    else:
        print("Lux Sensor Test Failed")
        gpio.output(lux_led, gpio.LOW)
        payloadPub("li",str(light_inten)+" : Failed")
        payloadPub("sr",str(solar_radi)+" : Failed")

    print("***********************************")


def setPointView():
    print("***********************************")
    print("Hardware Version: ", setP_hw)
    print("Firmware Version: ", setP_fw)
    print("Air Temperature min setpoint: ",
          setP_at_min, ", max setpoint: ", setP_at_max)
    print("Air Pressure min setpoint: ", setP_ap_min,
          ", Air Pressure max setpoint: ", setP_ap_max)
    print("Air Humidity min setpoint: ", setP_ah_min,
          "Air Humidity max setpoint: ", setP_ah_max)
    print("Leaf Wetness setpoint: ", setP_lw)
    print("Rain in MM setpoint: ", setP_rain)
    print("Wind Speed setpoint: ", setP_ws)
    print("Soil Temperature min setpoint: ", setP_at_min,
          ", Soil Temperature max setpoint: ", setP_st_max)
    print("Primery Soil Mositure min setpoint: ", setP_psm_min,
          "Primery Soil Mositure max setpoint: ", setP_psm_max)
    print("Secondary Soil Mositure min setpoint: ", setP_ssm_min,
          "Secondary Soil Mositure max setpoint: ", setP_ssm_max)
    print("Light Intensity Setpoint: ", setP_li)
    print("Solar Radiation: ", setP_rd)
    print("***********************************")


def mqttValueClear():
    client.publish("ds","")
    client.publish("sd","")
    client.publish("imei","")
    client.publish("ssm","")
    client.publish("psm","")
    client.publish("at","")
    client.publish("ap","")
    client.publish("ah","")
    client.publish("lw","")
    client.publish("ws","")
    client.publish("rc","")
    client.publish("wd","")
    client.publish("st","")
    client.publish("li","")
    client.publish("sr","")

#option for change the setpoint and check the setpoints --> This should happen before the main loop
def optionCheck():
    value = int(input(
        "1. For check the default values\n2. For change the default values\nPlease Enter the option:"))
    if value == 1:
        setPointView()
    elif value == 2:
        print("***********************************")
        setP_hw = float(input("Enter Hardware Version: "))
        setP_fw = float(input("Enter Firmware Version: "))
        setP_at_min = float(input("Enter Air Temperature Min Setpoint: "))
        setP_at_max = float(input("Enter Air Temperature Max Setpoint: "))
        setP_ap_min = float(input("Enter Air Pressure Min Setpoint: "))
        setP_ap_max = float(input("Enter Air Pressure Max Setpoint: "))
        setP_ah_min = float(input("Enter Air Humidity Min Setpoint: "))
        setP_ah_max = float(input("Enter Air Humidity Max Setpoint: "))
        setP_lw = int(input("Enter Leaf Wetness Setpoint: "))
        setP_rain = float(input("Enter Rain in mm Setpoint: "))
        setP_ws = float(input("Enter Wind speed Setpoint: "))
        setP_st_min = int(input("Enter Soil Temperature min Setpoint: "))
        setP_st_max = int(input("Enter Soil Temperature max Setpoint: "))
        setP_psm_min = int(input("Enter Primery Soil Moisture Min Setpoint: "))
        setP_psm_max = int(input("Enter Primery Soil Moisture Max Setpoint: "))
        setP_ssm_min = int(input("Enter Secondry Soil Mositure Min Setpoint: "))
        setP_ssm_max = int(input("Enter Secodary Soil Mositure Max Setpoint: "))
        setP_li = int(input("Enter Light Intersity Setpoint: "))
        setP_rd = int(input("Enter Solar Radation Level Setpoint: "))
        print("***********************************")
        print("")

    value = int(input("1. Home Menu\n2. Exit and Enter to the main Loop\nEnter the Option: "))
    if value == 1:
        optionCheck() #recursion funtion
    elif value == 2:
        print("Entering into the main loop")
    else:
        print("Entering into the main loop")

def gpioclean():
    gpio.output(ts_led, gpio.LOW)
    gpio.output(sd_led, gpio.LOW)
    gpio.output(imei_led, gpio.LOW)
    gpio.output(ssm_led, gpio.LOW)
    gpio.output(psm_led, gpio.LOW)
    gpio.output(bme_led, gpio.LOW)
    gpio.output(lw_led, gpio.LOW)
    gpio.output(ws_led, gpio.LOW)
    gpio.output(dr_led, gpio.LOW)
    gpio.output(st_led, gpio.LOW)
    gpio.output(lux_led, gpio.LOW)
    gpio.output(pass_led, gpio.LOW)
    gpio.output(ip_start, gpio.HIGH)
    gpio.output(pass_led, gpio.HIGH)

#this function should enable when using only in the raspberry Pi
#optionCheck()

def payloadPub(topic, payload):
    pubCheck = client.publish(topic, payload)
    while pubCheck[0]!=0:
        pubCheck = client.publish(topic, payload)
        time.sleep(0.1)

gpioclean()

setPointPub()
#main loop starts from here
while True:
    print("Press Start Button.. \nButton State: ", gpio.input(start_button),"\nReset Button: ", gpio.input(reset_button))
    time.sleep(1)
    ser.close()
    mqttValueClear()
    if gpio.input(start_button)==0:
        print("***********************************")
        print("Process Started!!")
        print("***********************************")
        temp =0
        ser.open()
        gpio.output(ip_start, gpio.LOW)
        gpio.output(pass_led, gpio.LOW)
        while temp==0:
            time.sleep(0.05)
            cc = ser.readline()
            cc = cc.rstrip('\r\n').lstrip() #remove r' (raw string)

           # cc = str(cc, 'utf-8') #remove b' (byte string to string)
        #    print(cc)
            if(len(cc) > 0):  #len should be greater than 0
                #print(".")
                payloadPub("serial", str(cc))
                print(cc)
                #time.sleep(0.5)
                if(cc == "Device Powered ON"):
                    print("Device Truned ON Successfuly")
                    gpio.output(ts_led, gpio.HIGH)
                    payloadPub("ds", "OK")
                if(cc == "Lux Available = 1"):
                    print("\n***********************************")
                    print("Lux Sensor Connected")
                    print("***********************************")

                if(cc == "Rain Counter Available = 1"):
                   print("\n***********************************")
                   print("Rain Sensor Connected")
                   print("***********************************")

                if(cc == "Rain counter initilization done.."):
                    print("\n***********************************")
                    print("Rain Counter Initilization Done. Do 4 Tik")
                    print("***********************************")

                if(cc == "<<< MSG: SD card initialization Successful! >>>"):
                    print("SD Card Detected Process Done")
                    gpio.output(sd_led, gpio.HIGH)
                    payloadPub("sd", "OK")


                if(cc == "mcu sleep"):
                    print("\n***********************************")
                    print("Sleep Mode")
                    print("***********************************")
                    temp=1

                if(cc[0] == '{'): #JSON fromat starts from {
                    tempJson = json.loads(cc)
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
                    check(imeiF, hw_ver, firm_ver, air_temp, air_pressure, air_humidity, leaf_wetness,
                    rain, wind_dir, wind_speed, soil_temp, p_soil_mois, s_soil_mois, light_int, solar_radi)

                    csvWrite(imeiF, hw_ver, firm_ver, air_temp, air_pressure, air_humidity, leaf_wetness,
                    rain, wind_dir, wind_speed, soil_temp, p_soil_mois, s_soil_mois, light_int, solar_radi)

            if gpio.input(reset_button)==0:
                print("\n***********************************")
                print("Process Stoped")
                print("***********************************")
                ser.close()
                temp = 1
        gpio.output(ip_start, gpio.HIGH)
        while gpio.input(reset_button)==1:
            #print(gpio.input(reset_button))
            time.sleep(1)
        gpioclean()



