import serial
import time
import json

ser = serial.Serial("COM7", 115200)

setP_hw = 3.0
setP_fw = 2.0
setP_at_min = 23.0
setP_at_max = 30.0
setP_ap_min = 8000.0
setP_ap_max = 10000.0
setP_ah_min = 40.0
setP_ah_max = 80.0
setP_lw = 20
setP_rain = 0.2
setP_ws = 0.2
setP_st_min = 20
setP_st_max = 32
setP_psm_min = 5900
setP_psm_max = 8000
setP_ssm_min = 5900
setP_ssm_max = 8000
setP_li = 2
setP_rd = 5

def check(imei, hw_ver, firm_ver, air_temp, air_pers, air_humidity, leaf_wetness, rain, wind_dir, wind_speed, soil_temp, p_soil_mois, s_soil_mois, light_inten, solar_radi):
    print("***********************************")
    if(len(imei)==15):
        print("IMEI Done")
    else:
        print("IMEI Failed")

    if(hw_ver==setP_hw):
        print("Hardware Version Done")
    else:
        print("Hardware Version Failed")

    if(firm_ver==setP_fw):
        print("Firmware Version Done")
    else:
        print("Firmware Version Failed")

    if(air_temp > setP_at_min and air_temp < setP_ah_max):
        print("Air Temperature Done")
    else:
        print("Air Temperature Failed")

    if(air_pres > setP_ap_min and air_pres < setP_ap_max):
        print("Air Pressure Done")
    else:
        print("Air Pressure Failed")

    if(air_humidity > setP_ah_min and air_humidity < setP_ah_max):
        print("Air Humidity Done")
    else:
        print("Air Humidity Failed")

    if(leaf_wetness > setP_lw):
        print("Leaf Wetness Done")
    else:
        print("Leaf Wetness Failed")

    if(rain > setP_rain):
        print("Rain Sensor Test Done")
    else:
        print("Rain Sensor Test Failed")

    if(len(wind_dir)>0):
        print("Wind Direction Done")
    else:
        print("Wind Direction Failed")

    if(wind_speed > setP_ws):
        print("Wind Speed Done")
    else:
        print("Wind Speed Failed")

    if(soil_temp > setP_st_min and soil_temp < setP_st_max):
        print("Soil Temperature Test Done")
    else:
        print("Soil Temperature Test Failed")

    if(p_soil_mois > setP_psm_min and p_soil_mois < setP_ah_max):
        print("Primery Soil Mositure Sensor Test Done")
    else:
        print("Primery Soil Mositure Sensor Test Failed")

    if(s_soil_mois > setP_ssm_min and s_soil_mois < setP_ssm_max):
        print("Secondary Soil Mositure Sensor Test Done")
    else:
        print("Secondary Soil Mositure Sensor Test Failed")

    if(light_inten > setP_li):
        print("Light Intensity Test Done")
    else:
        print("Light Intensity Test Failed")

    if(solar_radi > setP_rd):
        print("Solar Radiation Sensor Test Done")
    else:
        print("Solar Radiation Senor Test Failed")

    print("***********************************")

def optionCheck():
    value = int(input(
        "1. For check the default values\n2. For change the default values\nPlease Enter the option:"))
    if value == 1:
        print("***********************************")
        print("Hardware Version: ", setP_hw)
        print("Firmware Version: ", setP_fw)
        print("Air Temperature min setpoint: ", setP_at_min, ", max setpoint: ", setP_at_max)
        print("Air Pressure min setpoint: ", setP_ap_min, ", Air Pressure max setpoint: ", setP_ap_max)
        print("Air Humidity min setpoint: ", setP_ah_min, "Air Humidity max setpoint: ", setP_ah_max)
        print("Leaf Wetness setpoint: ", setP_lw)
        print("Rain in MM setpoint: ", setP_rain)
        print("Wind Speed setpoint: ", setP_ws)
        print("Soil Temperature min setpoint: ", setP_at_min, ", Soil Temperature max setpoint: ", setP_st_max)
        print("Primery Soil Mositure min setpoint: ", setP_psm_min, "Primery Soil Mositure max setpoint: ", setP_psm_max)
        print("Secondary Soil Mositure min setpoint: ", setP_ssm_min, "Secondary Soil Mositure max setpoint: ", setP_ssm_max)
        print("Light Intensity Setpoint: ", setP_li)
        print("Solar Radiation: ", setP_rd)
        print("***********************************")
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


optionCheck()

while True:
    cc = ser.readline()
    cc = cc.rstrip().lstrip()
    cc = str(cc, 'utf-8')
    #print(cc)
    if(len(cc) > 0):
        print(".")
        if(cc == 'Device Powered ON'):
            print("***********************************")
            print("Device on Ack received")
            print("***********************************")

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
            print("\n***********************************")
            print("SD Card Initialization Done")
            print("***********************************")

        if(cc == "mcu sleep"):
            print("\n***********************************")
            print("Sleep Mode")
            print("***********************************")


        if(cc[0] == '{'):
            tempJson = json.loads(cc)
            imei = tempJson.get("Z1")
            hw_ver = float(tempJson.get("Z4"))
            firm_ver = float(tempJson.get("Z8"))
            air_temp = float(tempJson["Z5"]["A"])
            air_pressure = float(tempJson["Z5"]["B"])
            air_humidity = float(tempJson["Z5"]["C"])
            leaf_wetness = int(tempJson["Z5"]["D"])
            rain = float(tempJson["Z5"]["E"])
            wind_dir = tempJson["Z5"]["F"]
            wind_speed = float(tempJson["Z5"]["G"])
            soil_temp = float(tempJson["Z5"]["H"])
            p_soil_mois = int(tempJson["Z5"]["I"])
            s_soil_mois = int(tempJson["Z5"]["J"])
            light_int = tempJson["Z5"]["O"]
            solar_radi = tempJson["Z5"]["P"]
            #print("IMEI number: ", tempJson.get("Z1"))
            print("***********************************")
            print("IMEI: ", imei)
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
            check(imei, hw_ver, firm_ver, air_temp, air_pressure, air_humidity, leaf_wetness,
            rain, wind_dir, wind_speed, soil_temp, p_soil_mois, s_soil_mois, light_int, solar_radi)
