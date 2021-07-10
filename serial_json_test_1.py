import serial
import time
import json

ser = serial.Serial("COM7", 115200)
bb = ""
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
            hw_ver = tempJson.get("Z4")
            firm_ver = tempJson.get("Z8")
            air_temp = tempJson["Z5"]["A"]
            air_pressure = tempJson["Z5"]["B"]
            air_humidity = tempJson["Z5"]["C"]
            leaf_wetness = tempJson["Z5"]["D"]
            rain = tempJson["Z5"]["E"]
            wind_dir = tempJson["Z5"]["F"]
            wind_speed = tempJson["Z5"]["G"]
            soil_temp = tempJson["Z5"]["H"]
            p_soil_mois = tempJson["Z5"]["I"]
            s_soil_mois = tempJson["Z5"]["J"]
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
