from pyboard_esp8266 import esp_pyboard
from pyb import UART, I2C
from HIH6130 import HIH6130
from V89 import V89Sensor
from Xbee_Driver import Xbee
from ppd42 import PPD42I2C
from analog_sensor import Analog_Sensor

#POLLING_DELAY = 120000  #the polling interval in miliseconds
CYCLE_INTERVAL = 2000   #length of time that controls the sensor gas read cycle



currentMillis = 0 #current elapsed time in milliseconds
pm0 = 0           #polling interval millis place holder
pm1 = 0           #secondary polling interval millis placeholder
cm0 = 0           #main cycle millis placeholder
deltaX = 0        #time between consecutive samples. Needed for calculating derivatives

POUT = False      #whether or not to print to console (useful for or'ing when calibrating)
CALIBRATING = False

##initialize sensor objects

ppm = 0                          #variable to hold the IAQ sensors CO2 data
trh = HIH6130()                  #temp and humidity data
v89 = V89Sensor()                #CO2 and VOC data
pm = PPD42I2C()                  #particulate matter data
pyBoard = esp_pyboard(2,115200)  #object that facilitates communication between esp8266 and pyboard
xbee = Xbee()                    #xbee object on UART 4, at 9600 baud that is used to send and receive data to/from the xbee module


#calling this function gets and saves the xbee mac address in the LowMacAddr data field of the xbee object
xbee.getLowMacAddr() 


##initialize Data history objects.
## Maintains a simple moving average, exponential moving average etc.
## Could have one for every data stream
CO2_History = Filters()

##byte array that will contain all the sensor data in the form 
## b'IAQ CO2, temp, humidity, CO2 V89, VOC V89, particulate matter\n'
wifi_data = bytearray()


##initialize an I2C bus on channel 2 as a master
i2c_bus2 = I2C(2, I2C.MASTER)             # create and init as a master
i2c_bus2.init(I2C.MASTER, baudrate=100000) # init as a master

#sends ssid,password,host,url values to esp8266 module so it can connect to wifi/server
#assumes the config file is present on the pyboard
pyBoard.sendConfigVars()
#pyBoard.isEsp8266Configured() #waits untill esp8266 tells pyboard it is connected to the internet


print("INIT PYBOARD")


#infinite loop
while True:
    
    pyb.delay(1000)
    currentMillis = pyb.millis()

##This block resends config variables should the esp reset
## at some point during the main loop. Testing has so far proven this unnecessary.
#
#   while(pyBoard.esp_uart.any()):
#
#       serialData = pyBoard.esp_uart.readline()
#
#       if(serialData == b'configuring\r\n'):
#           pyBoard.resendConfigVars()
        
        
    ##if the current reporting cycle has been exceeded
    ## time to get the sensor data again and transmit it to the
    ## esp amongst other things    
    if(((currentMillis - cm0) > CYCLE_INTERVAL) or (cm0 == 0)):
        
        
        print("CYCLE...\n");
        #uart_bus2.write("CYCLE...\n")

        # if(((currentMillis - pm0) > POLLING_DELAY) or (pm0 == 0)):
#             POUT = True
#             #save the last time we polled the sensors
#             pm0 = currentMillis
#         else:
#             POUT = False



        #read sensor data and save individual values to pyboard object
        #returns data as a byte-array in the format:
        #  CO2_ppm,temp,humidity,CO2,VOCs,particulate matter\n
        wifi_data = pyBoard.getSensorVals(i2c_bus2, ppm, pm, v89, trh)
        
        
        
        
        #open the CSV file that data will be logged too, write the data, close the file
        log = open('/sd/log.csv', 'a')
        log.write(wifi_data)
        log.close()
        
        #Get the time in milliseconds between the last sample was collected.
        #This is needed for calculating the slope/derivatives of the data
        deltaX = currentMillis - cm0
        
        #update CO2 data with newest sample and apply various filters to the data
        CO2_History.applyFilters(pyboard.getCO2_V89(),deltaX)
        
        #send gathered sensor data to esp8266
        pyBoard.sendSensorVals(wifi_data)
        
        ##write the sensor data to the UART bus
        uart_bus2.write(wifi_data)
        
        #makes output easier to read in the debugging stage
        if(CALIBRATING | POUT):
            uart.write("\n") #make the output easier to read

        led.toggle()
        
        #save the time this loop was entered
        cm0 = currentMillis
