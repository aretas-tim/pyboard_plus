from ADS1115_pyboard_plus import ADS1115

#on the pyboard plus board the CO sensor is connected to the ADS1115 ADC chip
#on channel 2, and the pyboard is connect to the ADS1115. So in order for the 
# To get a sensor reading a sensor reads the ADS1115 ADC on which in turn reads the sensor
# and returns a voltage to be read by the pyboard.

 


#The analog channel of the sensor is connected to the ADS1115.
#The ADS1115 firmware is written such that the analogue channels are 
# selected by choosing one of 'chan 0','chan 1','chan 2', 'chan 3'  

# main.py -- put your code here!
# from analog_calibration import Calibrator
# 
# 
# 
# usb = pyb.USB_VCP()
# voc_sensor = Analog_Sensor('Mocon VOC',1)
# co_sensor = Analog_Sensor('EC4-500-CO',2)
# sensor_list = [voc_sensor,co_sensor]
# calibration_routine = Calibrator(sensor_list)
# 
# while(True):
#     
#     print('outside loop')
#     
#     #usb.setinterrupt(-1)
#     if usb.any():
#         input = usb.readline()
#         #usb.close()
#         if b'calibrate' in input:
#             calibration_routine.calibrate()
#     else:
#         pyb.delay(1000)

class Analog_Sensor:
    
    # Data Fields-------------
    #
    # name: The name of the sensor as stated in the on_board_sensors.txt file
    # ADS1115: the object the gets the voltage readings of the sensor through the ADS1115 adc
    #           This object must be passed the I2C channel it is connect to the pyboard with ( 1 or 2)
    # i2c_channel: the channel the ADS1115 is connect to the pyboard with
    # type:the hexadecimal number aretas assigns every type of sensor used
    # adc_channel: the channel that the sensor is connected to on the ADS1115 
    #              (one of 'chan 0','chan 1','chan 2','chan 3',)
    # low_ppm: the concentration of the low concentration test gas (often zero air, so likely 0)
    # low_voltage: the voltage reading resulting from the low concentration test gas used in sensor calibration
    # high_ppm: the ppm of the high concentration test gas used in sensor calibration
    # high_voltage: the voltage reading resulting from the high concentration test gas used in sensor calibration
    # slope: the slope of the sensors voltage readings calculated through calibration
    #
    #
    # Note: it is important to instantiate an analoge sensor object with the name of the sensor given in the 
    #       on_board_sensors.txt file. Else, the object won't be able to automatically read in all its
    #       calibration data from the above file.
    
    def __init__(self,sensor_name,i2c=1):
         
        #save the name of the sensor
        self.name = sensor_name
        #instantiates an ADS1115 object that will be used to read the EC4-500-CO sensor
        #on i2c channel 1 of the pyboard
        self.ADS1115 = ADS1115(bus_num=i2c)
        #store the i2c channel the ads1115 chip is connected to on the Pyboard
        self.i2c_channel = i2c
        
        # The below block looks through the on_board_sensors.txt file for the name of the 
        # sensor that is being instantiated and reads in and parses:
        #   sensor name,sensor type,adc channel,low ppm, low voltage,high ppm, high voltage and slope data
        # it adds all these data points to a list.
        # Consult this file for a more detailed explanation of these data points
        
        #open the file that has all the data for the onboard sensors
        with open("on_board_sensors.txt") as f:
            sensor_data_list = [] 
            #read through each line of this file
            for line in f:
                # the line starts with the name of the sensor 
                if self.name in line:
                    
                    #while there is still data to be parsed in the line
                    while ':' in line:
                        #this finds the index of the next colon
                        eq_index = line.find(':')
                        #assigns anything before the colon to data
                        data = line[:eq_index]
                        #adds data to the list of sensor data
                        sensor_data_list.append(data)
                        #increments line to the beginning of the next data field
                        line = line[eq_index + 1:]
                    #the while loop continues until there is only one data field left and 0 :'s left
                    #thus we must save the final data field to the list of data
                    #this final data point also contains a '\n' character, so this is stripped     
                    sensor_data_list.append(line[:-1])
                else:
                    pass    

        f.close()
        
        #set the sensor type (hexadecimal value as assigned by aretas) of the sensor
        self.type = sensor_data_list[1]
        #set the channel that the sensor is connected to on the ADS1115 (one of 'chan 0','chan 1','chan 2','chan 3',)
        self.adc_channel = sensor_data_list[2]
        #set the ppm of the low concentration test gas used in sensor calibration
        self.low_ppm = sensor_data_list[3]
        #set the voltage reading resulting from the low concentration test gas used in sensor calibration
        self.low_voltage = sensor_data_list[4]
        #set the ppm of the high concentration test gas used in sensor calibration
        self.high_ppm = sensor_data_list[5]
        #set the voltage reading resulting from the high concentration test gas used in sensor calibration
        self.high_voltage = sensor_data_list[6]
        #set the slope of the sensors voltage readings calculated through calibration
        self.slope = sensor_data_list[7]
        #set the y-intercept of the sensors voltage readings calculated through calibration
        self.y_intercept = sensor_data_list[8]
         
         
         
         
         
      
    #returns a float that is the voltage reading in millivolts of the CO sensor
    #by reading the ADS1115 on whatever channel has been provided to the ADS1115 object on instantiation.     
    def getVoltageReading(self):
         
         millivolts = self.ADS1115.getSingleShotVoltage(self.adc_channel)
         return millivolts
         
    
         
    
         
    
        
         