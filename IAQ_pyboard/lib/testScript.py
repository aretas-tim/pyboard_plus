with open("/Users/timrogerson/Desktop/Work_Stuff/GIT Hub Firmware repositories/IAQ_Monitor_Untested/IAQ_pyboard/build/on_board_sensors.txt") as f:

    sensor_data_list = [] 
    #read through each line of this file
    for line in f:
        # the line starts with the name of the sensor 
        if 'Mocon VOC Sensor' in line:
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