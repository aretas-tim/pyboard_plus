import pyb
from pyb import UART


BUF_LENGTH=50

#enter command mode
atCmdMode = b"+++"
#get low serial number
atCmdSl = b"ATSL\r" 
#exit AT command mode
atCmdCn = b"ATCN\r" 
#set or read the PAN ID
atCmdID = b"ATID%x\r"
#write settings to nvram
atCmdWr = b"ATWR\r"


class Xbee:


    
    ##initializes the xbee onject with Uart bus 4, baud rate 9600 and 0 as its mac address
    def __init__(self, uart_bus=4, baud=9600):
 
 
        #initialize uart bus 4 on the pyboard for communication with xbee 
        self.xbee_uart = UART(uart_bus)
        self.xbee_uart.init(baud)
        #this is the data field for the mac address
        #it is a bytes object. NOT a string, or int, and must be handled accordingly
        self.LowMacAddr=b''
  
    ##Gets the low Mac address fromt he XBee unit and saves it into LowMacAddr data field
    ##This function calls enterCommandMode
    def getLowMacAddr(self):
        
        if(self.enterCommandMode()):
        
            #tell the Xbee to send the lower half of the Mac address
            self.xbee_uart.write(atCmdSl)
            pyb.delay(1000)
            #read all available characters from the xbee
            #this will be a bytes object
            response=self.xbee_uart.read()
            #print("the response from the xbee is:\n")
            #print(response)
            
            #the xbee returns the mac addres plus a '\r' character
            #this lines drops the "\r"
            response = response[:-1]
            #convert the bytes object mac address to an integer and
            self.LowMacAddr = response 
            #this line only for testing
            print("The mac address of the xbee on this board is:\n")
            print(self.LowMacAddr)
            
            #exit command mode
            self.xbee_uart.write(atCmdCn)
            pyb.delay(300)
            
            
        else:
            print("Did not recieve mac addres. something went wrong.")  
    
    
    def enterCommandMode(self):
    
        success = False
        #tell the Xbee you want it to enter command mode
        self.xbee_uart.write(atCmdMode)
        pyb.delay(1000)
        #read all available characters from the xbee
        response=self.xbee_uart.read()
        #if OK is in the byte string sent from XBee
        if b'OK' in response:
            success = True
        return success


# To DO!!!!!!!
# write a function that sends sensor value to the Xbee in the apropriate data format
# Gonna have to wait until The schematic for the pyboard plus is finalized.       
    def sendSensorVals(self,):
        

        
        
        
        
            
    
