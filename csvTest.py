from datetime import datetime 

try:
    now = datetime.now()
    fname = 'tReport_'+ str(now.strftime("%m%d%y%H%M%S"))+".csv"
    file = open(fname, "a")
    file.close()

except:
    print("File not Created!!")



