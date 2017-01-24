import sys
import pyb
from analog_sensor import Analog_Sensor








class Calibrator:
    
    states = ['initial','choose_sensor','input_gas_ppm','print_sensor_vals','enter_sensor_voltage','exit_calibration','check_user_input','idle','set_ppms','set_values','verify_ppms','verify_values','calc_slope_save']

    #the array that holds all the commands that the user can type into the monitor to initiate state change
    #any new commands that will be added must be added here and they must end with the appropriate delimiting character
    #as of writing this the delimiting character is "". so all the commands end with a ""
    #user_commands= [b"choose sensor",b"exit",b"pause", b"set values",b"set ppms",b"verify values",b"verify ppms",b"calc slope"]
    user_commands= ["choose sensor","exit","pause","set values","set ppms","verify values","verify ppms","calc slope"]
    
    def __init__(self, sensor_list):

        #A line of text entered by the user
        self.user_input=''
        #a variable used to keep track of the previous state
        self.prev_state = 'initial'
        #the variable used to keep track of the current state in the calibration routine
        self.curr_state = 'initial'
        #a flag used to ensure certain messages will only be printed once to the screen.
        #this reduces the clutter of the monitor when calibrating
        self.print_once_flag = False
        #the flag used to tell if the user has set the sensor values
        self.values_set=False
        #the flag used to tell if the user has set the ppm values
        self.ppms_set=False
        #the flag used to control when the calibration routine will be exited
        #initialized to true because the routine should not be enabled upon start up
        self.exit_routine=False
        
        #A list of sensor objects. See analog_sensor.py
        self.sensors=sensor_list
        #The current sensor selected for calibration. 
        self.current_sensor="none"
        
        
        
        
    def calibrate(self):

        #------Below block of code needed to reset all the flags in case the routine 
        #------is exited and re-entered in the same session
        #A line of text entered by the user
        self.user_input=''
        #a variable used to keep track of the previous state
        self.prev_state = 'initial'
        #the variable used to keep track of the current state in the calibration routine
        self.curr_state = 'initial'
        #a flag used to ensure certain messages will only be printed once to the screen.
        #this reduces the clutter of the monitor when calibrating
        self.print_once_flag = False
        #the flag used to tell if the user has set the sensor values
        self.values_set=False
        #the flag used to tell if the user has set the ppm values
        self.ppms_set=False
        #the flag used to control when the calibration routine will be exited
        #initialized to true because the routine should not be enabled upon start up
        self.exit_routine=False
        #The current sensor selected for calibration. 
        self.current_sensor="none"
        #--------#
        #--------#
                
        while not self.exit_routine:
        
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            #The initial state where a start message is printed to the screen
            if(self.curr_state == 'initial'):
                
                print("-------Calibration Started-------")
                #change to the idle state where
                
                
                
                self.change_state('idle')
                
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            #The idle state where input options are printed to the screen and user input is received    
            elif(self.curr_state =='idle'):
                
                if(self.print_once_flag == False):
                    
                    #print("\n")
                    
                    print('* The sensors that are on this board are: \n')
                    #print the name of all the sensors in the list of sensors passed to the calibration object
                    for s in self.sensors:
                        print("-"+s.name)
                    print("\n")
                    print("1) To select a sensor type the sensors name and press the return key")    
                    print("2) To pause enter \"pause\" and press the return key")
                    print("3) To set the sensor values type \"set values\" and press the return key")
                    print("4) To set the ppm values type \"set ppms\" and press the return key")
                    print("5) To print the current ppm values type \"verify ppms\" and press the return key")
                    print("6) To print the current sensor values type \"verify values\" and press the return key")
                    print("7) Calculate the sensor slopes and y-intercepts, and save value to pyboard, type \"calc slope\" and press the return key")
                    print("8) To exit type \"exit\"\n")
                    print("Waiting for user input..................")
                    print("-----------------------------------------------------------------")
                    print("-----------------------------------------------------------------")
                    #print("\n")
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
                    #print("sensor 1 name:")
                    #print(s.name)
                    #if the user entered the name of the sensor s
                    if(self.check_command(s.name)):
                    
                        print("You entered "+s.name+" .") 
                        print("This sensor is now selected.\n")
                        #change the sensor to the sensor the user entered
                        self.current_sensor = s
                        print("Any time you want to print the value of the sensor press the enter/return key.\n")
                        print("If you want to stop printing sensor values and select a different program function\n ")
                        print("press 'x' followed by the enter/return key.")
                        print("-------------------------------------------")
                        print("-------------------------------------------")                        
                        #proceed to the state that collects and prints out the current sensors measurements
                        self.change_state("print_sensor_vals")
                        #return the user_input data field to a blank string
                        #this lets us check if the user has entered anything
                        #self.user_input = ""
                
                #if the above block of code was run, and a sensor was selected
                # jump over the below code that continues to check user input against
                # the routine's commands    
                if(self.curr_state == "print_sensor_vals"):
                    pass
                #a sensor was not selected. Continue to check the user's input    
                else:   
                    #if input data matches the "exit" command 
                    if(self.check_command(self.user_commands[1])):
                
                        print("You typed \"exit\". Exiting calibration mode.")
                        #exit the calibration routine altogether
                        self.change_state("exit_calibration")
                    
                    
                    #if input data matches the "pause" command   
                    elif(self.check_command(self.user_commands[2])):
                
                        print("You typed \"pause\". Entering Idle mode.")
                        #proceed to the idle state that waits for user input
                        self.change_state("idle")
                    
                    #if input data matches the "set values" command      
                    elif(self.check_command(self.user_commands[3])):
                
                        print("You entered \"set values\".") 
                        print("Type the 2 sensor values you wish to use in the format \"low voltage,high voltage\".")
                        print("i.e 1.34,2.85 (no spaces, seperated by a comma). ")
                        #proceed to the state that collects and parses the voltage values of the on board sensors
                        self.change_state("set_values")
                    
                    #if input data matches the "set ppms" command      
                    elif(self.check_command(self.user_commands[4])):
                
                        print("You entered \"set ppms\".")
                        print("Type the 4 ppm values you wish to use in the format \"low ppm,hi ppm\".")
                        print("i.e 0.0,10.0 (no spaces, seperated by comma). ")
                        #proceed to the state that collects and parses the ppm values of the on board sensors
                        self.change_state("set_ppms")
                    
                    #if input data matches the "verify values" command     
                    elif(self.check_command(self.user_commands[5])):
                        if(self.current_sensor=="none"):
                            print("you have not selected a sensor. Please do so to continue.")
                            #proceed to the state that waits for user input
                            self.change_state("idle")
                        else:
                            print("You entered \"verify values\"")
                            print("The current sensor is: \n")
                            print(str(self.current_sensor.name)+"\n")
                            print("The low concentration voltage value is: ") 
                            print(str(self.current_sensor.low_voltage)+"\n")
                            print("The high concentration voltage value is: ") 
                            print(str(self.current_sensor.high_voltage)+"\n")
                    
                            #proceed to the state that waits for user input
                            self.change_state("idle")
                    
                    #if input data matches the "verify ppm" command
                    elif(self.check_command(self.user_commands[6])):
                        if(self.current_sensor=="none"):
                            print("you have not selected a sensor. Please do so to continue.")
                            #proceed to the state that waits for user input
                            self.change_state("idle")
                        else:
                            print("You entered \"verify ppms\"")
                            print("The current sensor is: \n")
                            print(str(self.current_sensor.name)+"\n")
                            print("The low concentration ppm is: ") 
                            print(str(self.current_sensor.low_ppm)+"\n")
                            print("The high concentration ppm is: ") 
                            print(str(self.current_sensor.high_ppm)+"\n")
                    
                            #proceed to the state that waits for user input
                            self.change_state("idle")
                    
                    #if input data matches the "calc slope" command
                    elif(self.check_command(self.user_commands[7])):
                
                        print("You entered \"calc slope\"")
                        #if the sensor values have been set
                        if(self.values_set == True):
                            #print(F("values_set: "))print(values_set)
                            #if the ppm values have been set
                            if(self.ppms_set == True):
                                #print(F("ppms_set: "))print(ppms_set)
                                #proceed to the state that calculates the slop and y-intercept of the 
                                #sensor's linear ouput
                                self.change_state("calc_slope_save")
                            else:
                                print("PPM values have not been set. Please do so to continue. ")
                                self.change_state("idle")
                        
                        else:
                            print("The sensor values have not been set. Please do so to continue. ")
                            self.change_state("idle")
                    else:
                        #the command entered by the user was not one of the legally recognizable options
                        print("\nDid not recognize command. Enter either: ")
                        print(self.user_commands[0])
                        print(self.user_commands[1])
                        print(self.user_commands[2])
                        print(self.user_commands[3])
                        print(self.user_commands[4])
                        print(self.user_commands[5])
                        print(self.user_commands[6])
                        print(self.user_commands[7])
                        #proceed to the state that waits for user input
                        self.change_state('idle')
            
            
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            # The state that allows the routine to exit back to the main loop       
            elif(self.curr_state =="exit_calibration"):
                self.exit_routine = True
            
                    
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            # The "print_sensor_vals" state where the value of the current sensor is printed to the screen anytime
            # the user presses the return/enter key. The state is exited if the user enters 'x' followed by the
            #  return/enter key.
            #                       
            elif(self.curr_state =="print_sensor_vals"): 
                
                #get the voltage reading from the current sensor via the ADS1115
                #voltage = self.current_sensor.getVoltageReading()
                #this dummy value used for testing
                voltage = 1.24
                #print the value to the screen
                print("Voltage reading for "+self.current_sensor.name+" : "+str(voltage))
                #get the user input
                self.getUserInput()
                #check to see if the user entered 'x'.
                #If so change to the idle state
                #if not stay in the "print sensor values" state
                if 'x' in self.user_input:
                    self.change_state("idle")
                    print(self.curr_state)
                
                    
                    
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            # The "set_values" state where a user enters the two voltage readings of the sensor observed
            # when applying a low concentration ppm gas and a high concentration ppm gas           
            elif(self.curr_state =='set_values'):
                
                if(self.current_sensor=='none'):
                    print("You have not selected a sensor yet. Can not set any values.")
                    print("-----------------------------------------------------------")
                    self.change_state("idle")
                else:    
                    print("in set_values state")
                    #get the user input
                    values = input()
                    #print the input to the screen so the user can see if she/he entered it
                    #correctly
                    print("you entered as low_voltage,high_voltage :")
                    print(values+"\n")
                    print("If this is correct enter \"y\" then press the enter key")
                    print("to enter another set of values enter any other letter then press the enter key")
                    #get the user's response to the above prompt
                    correct = input()
                    #if the user enteres "y" save the values to the sensor's data field and change state to "idle"
                    if('y' in correct):
                        # if input == '1.23,4.56', input.rpartition(',') looks like ('1.23', ',', '4.56') 
                        #saves first voltage value to the analog sensors low voltage data field
                        self.current_sensor.low_voltage = float(values.rpartition(',')[0])
                        #saves second voltage value to the analog sensors high voltage data field
                        self.current_sensor.high_voltage = float(values.rpartition(',')[2])
                        #sets the current state to idle
                        print("VALUES SET!!!")
                        self.change_state("idle")
                        #make values_set flag True
                        self.values_set=True
                    
                    else:
                        #remain in this state
                        self.change_state('set_values')
                        
                    
                    
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
                print(values+"\n")
                print("If this is correct enter \"y\" then press the enter key")
                print("to enter another set of ppms enter any other letter then press the enter key")
                #get the user's response to the above prompt
                correct = input()
                #if the user enteres "y" save the ppms to the sensor's data field and change state to "idle"
                if(correct == 'y'):
                    # if input == '1.23,4.56', input.rpartition(',') looks like ('1.23', ',', '4.56') 
                    #saves first voltage value to the analog sensors low voltage data field
                    self.current_sensor.low_ppm = float(values.rpartition(',')[0])
                    #saves second voltage value to the analog sensors high voltage data field
                    self.current_sensor.high_ppm = float(values.rpartition(',')[2])
                    #sets the current state to idle
                    self.change_state("idle")
                    #make ppms_set flag True
                    self.ppms_set=True
                else:
                    #remain in this state
                    self.change_state('set_ppms')
                    
                    
            
            #-------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------------------------#
            # The 'calc_slope_save' state where the slope of the current analog sensor is
            # calculated form the voltage readings produced formt he application of a low and high concentration
            # test gas.
            # Saving the new sensor data to a text file requires writing the new data to a new text file, deleting the old text file
            # and renaming the new file to the old one
                       
            elif(self.curr_state =='calc_slope_save'):
                
                #calculate the slope of the current sensor and save it to the appropriate data field
                self.current_sensor.slope = round(((self.current_sensor.high_ppm - self.current_sensor.low_ppm)/(self.current_sensor.high_voltage - self.current_sensor.low_voltage)),4)
                #calculate the y-intercept of the current sensor and save it to the appropriate data field
                self.current_sensor.y_intercept =  round(self.current_sensor.low_ppm - (self.current_sensor.slope*self.current_sensor.low_voltage),4)
                #create a string that has all the calibration data for the current sensor of the form "name:senor type:chan 0:low ppm:low voltage:high ppm:high voltage:slope:y_intercept"
                sensor_data = str(self.current_sensor.name)+":"+str(self.current_sensor.type)+":"+str(self.current_sensor.adc_channel)+":"+str(self.current_sensor.low_ppm)+":"+str(self.current_sensor.low_voltage)+":"+str(self.current_sensor.high_ppm)+":"+str(self.current_sensor.high_voltage)+":"+str(self.current_sensor.slope)+":"+str(self.current_sensor.y_intercept)+"\n"     
                
                #open the file that has the sensor data in read mode
                with open("on_board_sensors.txt","r") as file:
                    #reads file and stores each line in a list of lines
                    content = file.readlines()
                #close the file
                file.close()
                #gets the line number that contains the name of the current sensor (a list with a single element)
                #if there is one
                indices = [i for i, s in enumerate(content) if self.current_sensor.name in s]
                #if indices is empty (the current sensor name is not in the file we are checking)    
                if not indices:
                    print("The current sensor you have selected: ")
                    print(self.current_sensor.name)
                    print("is not in the file of on board sensors.")
                    print("Edit the file to incude it and try calibration again")
                    #change state back to idle
                    self.change_state('idle')
                #a line with the current sensor's name was found    
                else:        
                    #update the old line with the new calibration data
                    content[indices[0]] = sensor_data
                    #joins all the lines into a single string for writing back to the file    
                    new_string = ''.join(content)            
                    #open the file again, this time in write mode
                    with open("on_board_sensors.txt","w") as file:
                        #write the content back to the file
                        file.write(new_string)
                    #close the file
                    file.close()
                    print("slope and y-intercept saved to board!")
                    print("slope: "+str(self.current_sensor.slope))
                    print("y-intercept: "+str(self.current_sensor.y_intercept))
                    
                    #change state back to idle
                    self.change_state('idle')   
        
        #upon exiting the routine reset the state to initial
        #and return the exit flag to false
        self.change_state('initial')            
        self.exit_routine = False
        return         
                
                
                                      
                
                 
                
    #This function checks to see if the most recent user input stored in
    # the self.user_input data field is identical to the command string passed to it 
    #The command parameter is of type string           
    def check_command(self,command):
        # print("The cammand being checked is:")
#         print(command)
#         print("user_input is:")
#         print(self.user_input)
        
        is_command = False
        #if the command is equal to the most recent user input
        if(command==self.user_input):
            #print("command and user input are:")
            is_command = True
        
        #print(is_command)
        return is_command        
        
    
    
    #This function gets 1 line of user input. 
    #The function returns when it sees a new line character in the user input
    #a new line charater will result upon the hitting of the enter key
    def getUserInput(self):
        
        self.user_input = input()
        #self.user_input = sys.stdin.readline()
        #this line strips the new line character on input
        #self.user_input = self.user_input[:-1]
        
        
        
        
        
        
    #this function is used to change the state of the state machine    
    def change_state(self,next_state):
        
        #set the previous state to the current state
        self.prev_state = self.curr_state
        #set the current state to the next state
        self.curr_state = next_state
            
            
            
            
            
            
             
            
        
        
        
        
        
        
        
        
        