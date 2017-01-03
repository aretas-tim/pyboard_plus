##################################################################################################
# This Class contains functions that collect data from the sensors connected to the pyboard.     #
# It also contains functions that talk to the esp8266, feed the esp8266 configuration variables  #
# as well as sensor data to log on a server                                                      #
################################################################################################## 


import pyb
from pyb import UART

class esp_pyboard:

##Class constructor.
    def __init__(self, uart_bus=2, baud = 115200):
    
        #initialze uart bus 2
        self.esp_uart = UART(uart_bus)
        self.esp_uart.init(baud)
        
        #individual fields for sensor data
        self.temperature = b''
        self.humidity = b''
        self.CO2_V89 = b''
        self.tvoc_V89 = b''
        self.particulate = b''
        self.IAQ_ppm = b''
        
        
## esp8266 will print "configuring\r\n" repeatedly on start up 
## this function waits for that string and sends ssid, password, host and url
## It sends the config variables in the format: b'ssid,password,host,url'

    def sendConfigVars(self):
    
        ready = self.esp_uart.readline()
        print(ready)
        ##wait for "configuring\r\n" to continue
        while(not(ready == b'configuring\r\n')):
            pyb.delay(100)
            ready = self.esp_uart.readline()
            print("waiting")
        print("received start message from arduino")
        ###reading variables in config.txt into a dict and then sending them to esp8266
        vars = dict()
        with open("config.txt") as f:
            for line in f:
                eq_index = line.find(':')
                var_name = line[:eq_index].strip()
                number = line[eq_index + 1:].strip()
                vars[var_name] = number
        f.close()
        ##send config parameters to esp8266
        config_bytes = bytes(vars['ssid'],'utf-8')+b','+bytes(vars['password'],'utf-8') +b','+bytes(vars['host'],'utf-8')+b','+bytes(vars['url'],'utf-8')+b'\n'
        self.esp_uart.write(config_bytes)
        print(config_bytes)
        
        #############################################
        ## may want to write some code              #
        ## that continues to resend the config vars #
        ## untill the esp has sent an acknowledge   #
        #############################################
        
        
##esp8266 will print "configuring\r\n" if reset. 
##This function resends the config variables should the esp reset after initial start up
## It sends the config variables in the format: b'ssid,password,host,url

    def resendConfigVars(self):
         ###reading variables in config.txt into a dict and then sending them to esp8266
        vars = dict()
        with open("config.txt") as f:
            for line in f:
    
                eq_index = line.find(':')
                var_name = line[:eq_index].strip()
                number = line[eq_index + 1:].strip()
                vars[var_name] = number
        f.close()
        
        ##send config parameters to esp8266
        config_bytes = bytes(vars['ssid'],'utf-8')+b','+bytes(vars['password'],'utf-8') +b','+bytes(vars['host'],'utf-8')+b','+bytes(vars['url'],'utf-8')+b'\n'
        self.esp_uart.write(config_bytes)
        print(config_bytes)
       
       
       
## This function gets the data from the sensors, saves the values into the 
## pyboard objects data fields and returns a bytes object
## in the format b'IAQ CO2, temperature, humidity, v89_CO2, v89_VOC, particulate matter\n'  
    def getSensorVals(self,i2c, ppm, pm, v89, trh):  
      
        #create a buffer for sensor data
        i2c_data = bytearray(7)   
        
        print("GETTING i2c_data")
        
        #get data from IAQ sensor
        i2c.recv(i2c_data, 0x5A)
        ppm = i2c_data[0]
        ppm = ppm << 8
        ppm |= i2c_data[1]
        #save value to object fields
        self.IAQ_PPM = ppm
        print("IAQ ppm:")
        print(ppm)
        
        #write IAQ Data to serial/Xbee
        # uart.write("IAQ ppm:")
#         uart.write(str(ppm))
#         uart.write('\n')
        
        #get trh data from HIH6130
        trh.getTRH(i2c)
        #save temperature value to object field
        self.temperature = trh.temp
        print("TEMP:")
        print(str(trh.temp))
        #save humidity value to object field
        self.humidity = trh.rh
        print("HUMIDITY:")
        print(str(trh.rh))
        
        #get tvoc/CO2 data from V89 sensor
        v89.getData(i2c)
        #save CO2 value to object field
        self.CO2_V89 = v89.CO2
        print("CO2 EQUIV:")
        print(str(v89.CO2))
        #save vtoc value to object field
        self.tvoc_V89 = v89.tvoc
        print("TVOC~:")
        print(str(v89.tvoc))
        
        #get aprticulate data from ppd42 sensor
        pm.getData(i2c)
        self.particulate = pm.pm
        print("PARTICULATES:")
        print(str(pm.pm)) 
        
        return ppm+b','+trh.temp+b','+trh.rh+b','+v89.CO2+b','+v89.tvoc+b','+pm.pm+b'\n'           

## this function sends the data gathered by sensors to the esp8266

    def sendSensorVals(self,sensorVals):
    
        print("sending sensor values to esp8266")
        print(sensorVals) #printing to the screen for debug purposes
        self.esp_uart.write(sensorVals)
 
## a function that waits for a confirmation from the esp8226 that
## it is done configuring and connected to wifi. 
## Does not seem necessary after current testing.Currently not used in main script. 
        
    def isEsp8266Configured(self):
        
        pyb.delay(100)
        ready = self.esp_uart.readline()
        print(ready)
        
        while(not(ready == b'done configuring\r\n')):
            ready = self.esp_uart.readline()
            print("waiting for esp8266 to connect to wifi")
        print("esp8266 connected")
        
  
  
##################################################################################
## TO DO. Once Testing of the sensor in varying air quality conditions is done, ##
## This function will determine if the "Poor Quality" flag will be thrown.      ##
##################################################################################

    def determineAirQuality(self,):
        pass
        
        
        
#######################################################################
# getter functions to convert bytes object data fields to floats/ints #
# and return the values. Need integers for the signal processing      #
# and smoothing operations.                                           # 
#######################################################################        
    
    def getTemperature(self):
        
        bytes = self.temperature
        
        return float(bytes.decode('utf-8'))
        
    def getHumidity(self):
        
        bytes = self.humidity
        
        return float(bytes.decode('utf-8'))
        
        
    def getCO2_V89(self):
    
        bytes = self.CO2_V89
        
        return float(bytes.decode('utf-8'))
        
        
    def getTvoc_V89(self):
        
        bytes = self.tvoc_V89
        
        return float(bytes.decode('utf-8'))
        
        
    def getParticulate(self):
        
        bytes = self.particulate
        
        return float(bytes.decode('utf-8'))
        
        
    def getIAQ_ppm(self):
        
        bytes = self.IAQ_ppm
        
        return float(bytes.decode('utf-8'))
        

    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        



          