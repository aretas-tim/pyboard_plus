import sys
import pyb


states = ['initial','choose_sensor','input_gas_ppm','print_sensor_vals','enter_sensor_voltage','exit_calibration','check_user_input','idle','set_ppms','set_values','verify_ppms','verify_values','calc_slope_save']

#the array that holds all the commands that the user can type into the monitor to initiate state change
#any new commands that will be added must be added here and they must end with the appropriate delimiting character
#as of writing this the delimiting character is "". so all the commands end with a ""
user_commands= [b"choose sensor",b"exit",b"pause", b"set values",b"set ppms",b"verify values",b"verify ppms",b"calc slope"]

#the parseing function uses the strtok() function which requires a string with all the delimiting characters. 
#In this case, the parsed values will be seperated by "," and the entered string will be terminated with ""
parsing_delimiters = [b",",b";"]



class Calibrator:

    def __init__(self, input_delimiter, sensor_list)

        #A line of text entered by the user
        self.user_input=""
        #a variable used to keep track of the previous state
        self.prev_state = check_user_input
        #the variable used to keep track of the current state in the calibration routine
        self.curr_state = check_user_input
        #a flag used to ensure certain messages will only be printed once to the screen.
        #this reduces the clutter of the monitor when calibrating
        self.print_once_flag = False
        #the flag used to tell if the user has set the sensor values
        self.values_set=False
        #the flag used to tell if the user has set the ppm values
        self.ppms_set=False
        #the flag used to control when the calibration routine will be exited
        #initialized to true because the routine should not be enabled upon start up
        #self.exit_routine=True
        
        #A list of sensor objects. See analog_sensor.py
        self.sensors=sensor_list
        #the character used to denote the end of user input
        self.delimiter = input_delimiter
        #The current sensor selected for calibration. 
        self.current_sensor="none"
        
        
    def calibrate(self):
        
        exit_routine = False
        
        while(!exit_routine):
        
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            #The initial state where a start message is printed to the screen
            if(self.curr_state == 'initial'):
                
                print("-------Calibration Started-------\n\n")
                #change to the idle state where
                self.change_state('idle')
                
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            #The idle state where input options are printed to the screen and user input is received    
            elif(self.curr_state =='idle'):
                
                if(self.print_once_flag == False):
                    print("\n")
                    print("To select a sensor enter 'choose' and press the return key\n")
                    print("To pause enter \"pause\" and press the return key ")
                    print("To set the 4 sensor values type \"set values\" and press the return key")
                    print("To set the 4 ppm values type \"set ppms\" and press the return key")
                    print("To print the current ppm values type \"verify ppms\" and press the return key")
                    print("To print the current sensor values type \"verify values\" and press the return key")
                    print("Calculate the sensor slopes and y-intercepts, and write them to EEPROM type \"calc slope\" and press the return key")
                    print("To exit type \"exit\"")
                    print("\n")
                    print("Waiting for user input..................")
                    print("\n")
                    self.print_once_flag = True
                
                #get a line of user input
                self.getUserInput()
                #change to the state where the user input is verified
                self.change_state("check_user_input") 
                #return the print_once_flag is set back to false so future messages will be printed
                self.print_once_flag = False
            
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            #the state where the user chooses which sensor to calibrate
            elif(self.curr_state =='choose_sensor'):
            
                if(self.print_once_flag == False):
                    print("\n\n")
                    print('The sensors on this board are: ')
                    for s in self.sensors:
                        print("--- "+s.name+'\n')
                        
                    print("To select a sensor type its name exactly as you see it above and press enter.")
                    self.print_once_flag = True
                    
                #get a line of user input
                self.getUserInput()
                #change to the state where the user input is verified
                self.change_state("check_user_input") 
                #return the print_once_flag is set back to false so future messages will be printed
                self.print_once_flag = False
                
                
                            
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            #The check_user_input state where user input is compared to predetermined commands and state is
            #changed based on the user input
            elif(self.curr_state =="check_user_input"):
            
                #for each sensor in the list of sensors
                for s in self.sensors:
                    #if the user entered the name of the sensor s
                    if(check_command(s.name):
                    
                        print("You entered "+s.name+" ." 
                        print("This sensor is now selected.\n")
                        #change the sensor to the sensor the user entered
                        self.current_sensor = s
                        print("Any time you want to print the value of the sensor press the enter/return key.\n")
                        print("If you want to stop printing sensor values and select a different program function\n ")
                        print("press 'x' followed by the enter/return key.")
                        
                        #proceed to the state that collects and prints out the current sensors measurements
                        self.change_state("print_sensor_vals")
                        #return the user_input data field to a blank string
                        #this lets us check if the user has entered anything
                        self.user_input = ""
                    
                   
                #if input data matches the "exit" command 
                if(check_command(user_commands[1])):
                
                    print("You typed \"exit\". Exiting calibration mode."))
                    #exit the calibration routine altogether
                    change_state("exit_calibration")
                    self.exit_routine = true
                    
                #if input data matches the "pause" command   
                elif(check_command(user_commands[2])):
                
                    print("You typed \"pause\". Entering Idle mode."))
                    #proceed to the idle state that waits for user input
                    self.change_state("idle")
                    
                #if input data matches the "set values" command      
                elif(check_command(user_commands[3])):
                
                    print("You entered \"set values\".")) 
                    print("Type the 2 sensor values you wish to use in the format \"low voltage,high voltage\"."))
                    print("i.e 1.34,2.85 (no spaces, seperated by a comma). "))
                    #proceed to the state that collects and parses the voltage values of the on board sensors
                    self.change_state("set_values")
                    
                #if input data matches the "set ppms" command      
                elif(check_command(user_commands[4])):
                
                    print("You entered \"set ppms\".")) 
                    print("Type the 4 ppm values you wish to use in the format \"low ppm,hi ppm\"."))
                    print("i.e 0.0,10.0 (no spaces, seperated by comma). "))
                    #proceed to the state that collects and parses the ppm values of the on board sensors
                    self.change_state("set_ppms")
                    
                #if input data matches the "verify values" command     
                elif(check_command(user_commands[5])):
                
                    print("You entered \"verify values\"")
                    print("The current sensor is: \n")
                    print(self.current_sensor.name+"\n")
                    print("The low concentration voltage value is: ") 
                    print(self.current_sensor.low_voltage+"\n")
                    print("The high concentration voltage value is: ") 
                    print(self.current_sensor.high_voltage)
                    
                    #proceed to the state that waits for user input
                    self.change_state("idle")
                    
                #if input data matches the "verify ppm" command
                elif(check_command(user_commands[6])):
                
                    print("You entered \"verify ppms\"")
                    print("The current sensor is: \n")
                    print(self.current_sensor.name+"\n")
                    print("The low concentration ppm is: ") 
                    print(self.current_sensor.low_ppm+"\n")
                    print("The high concentration ppm is: ") 
                    print(self.current_sensor.high_ppm)
                    
                    #proceed to the state that waits for user input
                    self.change_state("idle")
                    
                #if input data matches the "calc slope" command
                elif(check_command(user_commands[7])):
                
                    print("You entered \"calc slope\"")
                    #if the sensor values have been set
                    if(self.values_set == true):
                        #print(F("values_set: "))print(values_set)
                        #if the ppm values have been set
                        if(self.ppms_set == true):
                            #print(F("ppms_set: "))print(ppms_set)
                            #proceed to the state that calculates the slop and y-intercept of the 
                            #sensor's linear ouput
                            self.change_state("calc_slope_save")
                        else:
                            print("PPM values have not been set. Please do so to continue. ")
                        
                    else:
                        print("The sensor values have not been set. Please do so to continue. ")
                     
                else:
                    #the command entered by the user was not one of the legally recognizable options
                    print("Did not recognize command. Enter either: ")
                    print(user_commands[0])
                    print(user_commands[1])
                    print(user_commands[2])
                    print(user_commands[3])
                    print(user_commands[4])
                    print(user_commands[5])
                    print(user_commands[6])
                    print(user_commands[7])
                    #proceed to the state that waits for user input
                    self.change_state(idle)
                    
                    
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            # The "print_sensor_vals" state where the value of the current sensor is printed to the screen anytime
            # the user presses the return/enter key. The state is exited if the user enters 'x' followed by the
            #  return/enter key.
            #
            elif(self.curr_state =="print_sensor_vals"): 
                
                #get the voltage reading from the current sensor via the ADS1115
                voltage = self.current_sensor.getVoltageReading()
                #print the value to the screen
                print("Voltage reading for "+self.current_sensor.name+" : "+str(voltage))
                #get the user input
                input = input()
                #check to see if the user entered 'x'.
                #If so change to the idle state
                #if not stay in the "print sensor values" state
                if input != 'x':
                    self.curr_state =="print_sensor_vals"
                else:
                    self.curr_state =="idle"
                    
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            # The "set_values" state where a user enters the two voltage readings of the sensor observed
            # when applying a low concentration ppm gas and a high concentration ppm gas           
            elif(self.curr_state =='set_values'):
                
                #get the user input
                values = input()
                #print the input to the screen so the user can see if she/he entered it
                #correctly
                print("you entered as low_voltage,high_voltage :")
                print(input+"\n")
                print("If this is correct enter \"y\" then press the enter key")
                print("to enter another set of values enter any other letter then press the enter key")
                #get the user's response to the above prompt
                correct = input()
                #if the user enteres "y" save the values to the sensor's data field and change state to "idle"
                if(correct == 'y'):
                    # if input == '1.23,4.56', input.rpartition(',') looks like ('1.23', ',', '4.56') 
                    #saves first voltage value to the analog sensors low voltage data field
                    self.current_sensor.low_voltage = float(input.rpartition(',')[0])
                    #saves second voltage value to the analog sensors high voltage data field
                    self.current_sensor.high_voltage = float(input.rpartition(',')[2])
                    #sets the current state to idle
                    self.curr_state =="idle"
                    #make values_set flag True
                    self.values_set=True
                    
                else:
                    #remain in this state
                    self.curr_state =='set_values'
                    
                    
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            # The "set_ppms" state where a user enters the two voltage readings of the sensor observed
            # when applying a low concentration ppm gas and a high concentration ppm gas           
            elif(self.curr_state =='set_ppms'):
                
                #get the user input
                values = input()
                #print the input to the screen so the user can see if she/he entered it
                #correctly
                print("you entered as low_ppm,high_ppm :")
                print(input+"\n")
                print("If this is correct enter \"y\" then press the enter key")
                print("to enter another set of ppms enter any other letter then press the enter key")
                #get the user's response to the above prompt
                correct = input()
                #if the user enteres "y" save the ppms to the sensor's data field and change state to "idle"
                if(correct == 'y'):
                    # if input == '1.23,4.56', input.rpartition(',') looks like ('1.23', ',', '4.56') 
                    #saves first voltage value to the analog sensors low voltage data field
                    self.current_sensor.low_ppm = float(input.rpartition(',')[0])
                    #saves second voltage value to the analog sensors high voltage data field
                    self.current_sensor.high_ppm = float(input.rpartition(',')[2])
                    #sets the current state to idle
                    self.curr_state =="idle"
                    #make ppms_set flag True
                    self.ppms_set=True
                else:
                    #remain in this state
                    self.curr_state =='set_ppms'
                    
                    
            
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            # The 'calc_slope_save' state where the slope of the current analog sensor is
            # calculated form the voltage readings produced formt he application of a low and high concentration
            # test gas.
            # Saving the new sensor data to a text file requires writing the new data to a new text file, deleting the old text file
            # and renaming the new file to the old one
                       
            elif(self.curr_state =='calc_slope_save'):
            
                #calculate the slope of the current sensor and save it to the appropriate data field
                self.current_sensor.slope = (self.current_sensor.high_voltage - self.current_sensor.low_voltage)/(self.current_sensor.high_ppm - self.current_sensor.low_ppm)
                #calculate the y-intercept of the current sensor and save it to the appropriate data field
                self.current_sensor.y_intercept =  self.current_sensor.low_ppm - (self.current_sensor.slope*self.current_sensor.low_voltage)
                #create a string that has all the calibration data for the current sensor of the form "name:senor type:chan 0:low ppm:low voltage:high ppm:high voltage:slope:y_intercept"
                sensor_data = self.current_sensor.name+":"+self.current_sensor.type+":"+self.current_sensor.adc_channel+":"+self.current_sensor.low_ppm+":"+self.current_sensor.low_voltage+":"+self.current_sensor.high_ppm+":"+self.current_sensor.high_voltage+":"+self.current_sensor.slope+":"+self.current_sensor.y_intercept     
                #open the file that has the sensor data AND create a new file for the new sensor data
                #this process is necessary because  micropython doesn't support inline changes to files
                with open("on_board_sensors.txt") as old_file, open("new_file.txt",'w') as new_file:
                #read through each line of this file
                for line in old_file:
                    # if the line starts with the name of the sensor 
                    if self.current_sensor.name in line:
                        #write the new sensor data to the file
                        new_file.write(sensor_data)
                    else:
                        new_file.write(line)    
                #close the files
                old_file.close()
                new_file.close()
                #delete the old sensor data file
                os.remove("on_board_sensors.txt")
                #rename the new file with the new sensor data to "on_board_sensors.txt"
                os.rename("new_file.txt","on_board_sensors.txt")    
                    
                    
                
                
                
                                      
                
                 
                
    #This function checks to see if the most recent user input stored in
    # the self.user_input data field is identical to the command string passed to it 
    #The command parameter is of type string           
    def check_command(self,command):
        
        is_command = False
        #if the command is equal to the most recent user input
        if(command==self.user_input):
            is_command = True
        
        return is_command        
        
    
    
    #This function gets 1 line of user input. 
    #The function returns when it sees a new line character in the user input
    #a new line charater will result upon the hitting of the enter key
    def getUserInput(self):
        
        self.user_input = sys.stdin.readline()
        
        #self.user_input = input()
        
        
        
        
    #this function is used to change the state of the state machine    
    def change_state(self,next_state):
        
        #set the previous state to the current state
        self.prev_state = self.curr_state
        #set the current state to the next state
        self.curr_state = next_state
            
            
            
            
            
            
             
            
        
        
        
        
        
        
        
        
        