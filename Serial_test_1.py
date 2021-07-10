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
    if(len(cc)>0):
        print(".")
        if(cc == 'Device Powered ON'):
            print("Device on Ack received")
            print(cc)

        if(cc[0]=='{'):
            tempJson = json.loads(cc)
            imei = tempJson.get("Z1")
            hw_ver = tempJson.get("Z4")
            firm_ver = tempJson.get("Z8")
            air_temp = tempJson.get("A")
            air_pressure = tempJson.get("B")
            air_humidity = tempJson.get("C")
            leaf_wetness = tempJson.get("D")
            rain = tempJson.get("E")
            wind_dir = tempJson.get("F")
            wind_speed = tempJson.get("G")
            soil_temp = tempJson.get("H")
            p_soil_mois = tempJson.get("I")
            s_soil_mois = tempJson.get("J")
            light_int = tempJson.get("O")
            solar_radi = tempJson.get("P")
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



