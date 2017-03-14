from pyboard_esp8266 import esp_pyboard
from pyb import UART, I2C
from HIH6130 import HIH6130
from V89 import V89Sensor
from Xbee_Driver import Xbee
from ppd42 import PPD42I2C
from analog_sensor import Analog_Sensor
from analog_calibration import Calibrator

#POLLING_DELAY = 120000  #the polling interval in miliseconds
#length of time that controls the sensor gas read cycle
CYCLE_INTERVAL = 2000    
#the length of time the script waits before checking 
#if any characters have been sent via the USB port
USB_INTERVAL = 3000      



currentMillis = 0 #current elapsed time in milliseconds
usb_millis = 0           #polling interval millis place holder
cm0 = 0           #main cycle millis placeholder
deltaX = 0        #time between consecutive samples. Needed for calculating derivatives
POUT = False      #whether or not to print to console (useful for or'ing when calibrating)
CALIBRATING = False

#initialize and LED for indication purposes
led = pyb.LED(2)

##initialize sensor objects

ppm = 0                             #variable to hold the IAQ sensors CO2 data
trh = HIH6130()                     #temp and humidity data
v89 = V89Sensor()                   #CO2 and VOC data
pm = PPD42I2C()                     #particulate matter data
pyBoard = esp_pyboard(2,115200)     #object that facilitates communication between esp8266 and pyboard
xbee = Xbee()                       #xbee object on UART 4, at 9600 baud that is used to send and receive data to/from the xbee module
usb = pyb.USB_VCP()                 #the object used to listen to the usb serial line. Used for entering into calibration mode

#The VOC analog sensor object. Initialized with 
#the name of the VOC sensor in the "on_board_sensors.txt" and the
#analog input channel the sensor is connected to on the ADS1115 chip
voc_sensor = Analog_Sensor('Mocon VOC',1) 

#The CO analog sensor object. Initialized with 
#the name of the CO sensor in the "on_board_sensors.txt" and the
#analog input channel the sensor is connected to on the ADS1115 chip    
co_sensor = Analog_Sensor('EC4-500-CO',2)

#initializes a Calibrator object used to calibrate analog_sensor objects passed to it.
#the analog sensors must be passed in the form of a list
calibrator = Calibrator([voc_sensor,co_sensor])         





 
#calling this function gets and saves the xbee mac address in the LowMacAddr data field of the xbee object
mac_addr = xbee.getLowMacAddr() 


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
    
    pyb.delay(2000)
    currentMillis = pyb.millis()
    
    #if USB polling interval has been exceeded, check for any input characters
    if(((currentMillis - usb_millis) > USB_INTERVAL) or (usb_millis == 0)):
    
    ######################################################################
    #this block enters into the calibration state machine if it receives #
    #'cal' via the pyboard's usb port through a terminal on a computer   #
    ######################################################################
        if(usb.any()):
            #read a line (or available characters) in the usb buffer
            user_input = usb.readline()
            #if "cal" is contained in the user's input
            if("cal" in user_input):
                #enter the calibration routine with the sensors passed to the
                #calibration object on the start of this main script
                #the calibration routine will not exit until the user
                # types "exit" while the routine is running
                calibrator.calibrate()
        usb_millis = currentMillis
            
            

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
