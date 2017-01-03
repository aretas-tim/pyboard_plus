############################################################################################
# This Class contains functions that keep a moving window of Raw Sensor data,              #      
# simple moving averages, exponential moving averages, svitzky-golay approximations,       #
# first derivatives, second derivatives and largrange approximations of first derivatives. #
# One filter object will be created for each data stream. This class is currently untested.#                                                       #
############################################################################################
import math

class Filters:
    
    ########################################################
    ## Data Point History and initialization              ##
    ########################################################
    
    ##number of Data samples in the history
    WINDOW_LENGTH = 10
    ##list to hold the previous sample points
    sample_history = [0]*WINDOW_LENGTH
    
    ########################################################
    ## Simple Moving Average constants and initialization ##
    ########################################################
 
    #window length for simple moving average
    SMA_LENGTH = 10 
    ##list to hold the previous SMA history
    sma_history =  [0]*SMA_LENGTH
    
    
    #############################################################
    ## Exponential Moving Average constants and initialization ##
    #############################################################
 
    #Weighting coefficient for exponential moving average. 
    #A value between 0 and 1.
    EMA_ALPHA = 0.1 
    #window length for simple moving average
    EMA_LENGTH = 10 
    ##list to hold the previous EMA history
    ema_history =  [0]*EMA_LENGTH
    
           
    ########################################################
    ## Savitzky-Golay Filter constants and initialization ##
    ########################################################


    #Window length for SGA filter. Value can be 5, 7, 9
    # For VALUE ARRAY length 5, only quadratic or cubic smoothing may be used 
    SGA_VALUE_LENGTH = 5
    #The array for the history of SGA approximations
    SGA_HISTORY_LENGTH = 10
    #the index of the middle bucket in the SGA VALUE array
    SGA_MID = int(SGA_VALUE_LENGTH/2)
    
    #A array of values neede to calculate the SGA approximation
    #At any given time the middle bucket contains the most recent calculation
    sga_values = [0]*SGA_VALUE_LENGTH
    
    #list to act as history of sga data points
    sga_history = [0]*SGA_HISTORY_LENGTH

    #For quadratic or cubic smoothing, enter degree 3. 
    #For quartic or quintic smoothing, enter degree 4.*/
    SGA_DEGREE = 3 

    SGA_INDEX = (SGA_DEGREE - SGA_VALUE_LENGTH + 2)

    # Do not change
    SGA_MAX_LENGTH = 9  

    # Coefficients needed in the lagrange polynomial approximation of this algorithm
    SGA_COEFFICIENTS = [[0, 0, -3, 12, 17, 12, -3, 0, 0],
                        [-21, 14, 39, 54, 59, 54, 39, 14, -21],
                        [15, -55, 30, 135, 179, 135, 30, -55, 15],
                        [0, -2, 3, 6, 7, 6, 3, -2, 0],
                        [0, 5, -30, 75, 131, 75, -30, 5, 0]]


    SGA_NORMALIZATION_VAL = 0
 
    ########################################################
    ## Derivative constants and initialization            ##
    ########################################################
    
    ##Number of previous first derivatives to be stored (using lagrange approximation)
    LAGRANGE_LENGTH = 10 
    ##list to hold the previous sample points
    lagrange_history =  [0]*LAGRANGE_LENGTH
    
    ##Number of previous first derivatives to be stored (using classical method)
    SLOPE_LENGTH = 10 
    ##list to hold the previous sample points
    slope_history =  [0]*SLOPE_LENGTH
    
    ##Number of previous 2nd derivatives to be stored (using classical method)
    SECOND_ORDER_LENGTH = 10 
    ##list to hold the previous sample points
    secondOrder_history =  [0]*SECOND_ORDER_LENGTH
    
 
    ##Constructor for the Class. 
    ##Calculates the  Normalization values for SGA algorithm
    ##Initializes current data fields to 0
    def __init__(self):
        
        #calc the normalization value for Savitzky-Golay Filter
        
        for i in range(self.SGA_MAX_LENGTH):
            self.SGA_NORMALIZATION_VAL += self.SGA_COEFFICIENTS[self.SGA_INDEX][i]
        
        #initializing to fields to 0
        self.SMA = 0
        self.EMA = 0
        self.SGA = 0
        self.lagrange_deriv = 0
        self.slope = 0
        self.secondOrder = 0
    
    
     
    ## This function adds the new a data sample to the sample history from the left.
    ## The moving window is currently 10 sample long. Change WINDOW_LENGTH to increase.
    def updateSampleHistory(self, new_sample):
    
        #push every value to the left by one
        self.sample_history[:] = self.sample_history[1:]+[self.sample_history[0]]
            
        #push the current value into the list from the left
        self.sample_history[self.WINDOW_LENGTH-1] = new_sample  
        
        
        
        
    ## This function calculates a simple moving average 
    ## and adds the new data to the SMA history from the left.
    ## The moving window is currently 10 sample long. Change SMA_LENGTH to increase.    
    def simpleMovingAverage(self):

        sample_sum = 0
        
        # if (self.SMA < 0 ):
#             self.SMA = 0
            
        #push every value to the left by one
        self.sma_history[:] = self.sma_history[1:]+[self.sma_history[0]] 
        
        # sum all the values in the sample history
        sample_sum = sum(self.sample_history)
        
        #calculate the smiple moving average and round to 3 decimal places
        self.SMA = round(sample_sum/self.WINDOW_LENGTH,3)
        
        #push the current average into the SMA history from the left
        self.sma_history[self.SMA_LENGTH-1] = self.SMA
        
        return self.SMA
    
    
    
    ## This function calculates an exponential moving average 
    ## and adds the new data to the EMA history from the left
    ## The moving window is currently 10 sample long. Change EMA_LENGTH to increase. 
    def exponentialMovingAverage(self):
        
       #  if (self.EMA < 0 ):
#             self.EMA = 0
            
        #push every value in the EMA HISTORY data structure to the left by one
        self.ema_history[:] = self.ema_history[1:]+[self.ema_history[0]]
         
        #calculate the EMA for the newest data point        
        self.EMA = (self.EMA_ALPHA*self.sample_history[self.WINDOW_LENGTH-1] + (1-self.EMA_ALPHA)*self.EMA)
        
        #push the current average into the EMA history from the left, round it to 3 decimal places
        self.ema_history[self.EMA_LENGTH-1] = round(self.EMA,3)
        
        return self.EMA 
        
    ## This function calculates a Savitzky-Golay approximation of the raw data
    ## and adds the new data to the SGA history from the left. This algorithm smooths the 
    ## raw data less than a simple moving average. Might not be necessary. 
    ## The moving window is currently 10 sample long. Change SGA_LENGTH to increase. 
    def savitzkyGolayFilter(self):
        
        # if (self.SGA < 0 ):
#             self.SGA = 0
            
        sum = 0
        
        #push every SGA approximation to the left by one
        self.sga_history[:] = self.sga_history[1:]+[self.sga_history[0]]
        
        #push every SGA value to the left by one
        self.sga_values[:] = self.sga_values[1:]+[self.sga_values[0]]
        
    
        #push the newest sample into the SGA values from the left
        self.sga_values[self.SGA_VALUE_LENGTH-1] = self.sample_history[self.WINDOW_LENGTH-1]
        
        for i in range(-self.SGA_MID,self.SGA_MID+1):
            sum += self.sga_values[i+self.SGA_MID]*self.SGA_COEFFICIENTS[self.SGA_INDEX][i+self.SGA_MID]
         
        #insert the SGA approximation into the value array in the middle bucket      
        self.sga_values[self.SGA_MID]=round(sum/self.SGA_NORMALIZATION_VAL ,3)
        
        #Push the current approximation onto the SGA history
        self.sga_history[-1]=self.sga_values[self.SGA_MID]
        
        return self.sga_history[self.SGA_MID]
        

    ## This function approximates the first derivative of the raw data via Langrange approximation
    ## and adds the new value to its history from the left.
    ## The moving window is currently 10 sample long. Change LAGRANGE_LENGTH to increase. 
    ## deltaX is the time between the most recent consecutive samples
    def lagrangeDerivative(self, deltaX):
        
        # lagrangian approximation for the first derivative of a function
        # calculated from the three most recent sample points.
        # function currently uses SMA sample history. May just want to
        # have a unified sample history that all functions in the class use
        self.lagrange_deriv = ((-3)*self.sample_history[self.WINDOW_LENGTH-3]+4*self.sample_history[self.WINDOW_LENGTH-2]-1*self.sample_history[self.WINDOW_LENGTH-1])/(2*deltaX)
        
        #push every value to the left by one
        self.lagrange_history[:] = self.lagrange_history[1:]+[self.lagrange_history[0]]
         
        #push the current average into the EMA history from the left
        self.lagrange_history[self.LAGRANGE_LENGTH-1] = self.lagrange_deriv
                                    
        return self.lagrange_deriv
    
    ## This function approximates the slope of the raw data via the classical method
    ## and adds the new value to the slope history from the left. 
    ## The moving window is currently 10 samples long. Change SLOPE_LENGTH to increase. 
    ## deltaX is the time between the most recent consecutive samples   
    def getSlope(self, deltaX):
        
        self.slope = (self.sample_history[self.WINDOW_LENGTH-1]-self.sample_history[self.WINDOW_LENGTH-2])/deltaX
         
        #push every value to the left by one
        self.slope_history[:] = self.slope_history[1:]+[self.slope_history[0]]
         
        #push the current first order derivative into the  history from the left
        self.slope_history[self.SLOPE_LENGTH-1] = self.slope
                                
        return self.slope
        
    ## This function approximates the 2nd derivative of the raw data via the classical method
    ## and adds the new value to its history from the left.
    ## The moving window is currently 10 sample long. Change SECOND_ORDER_LENGTH to increase. 
    ## deltaX is the time between the most recent consecutive samples
    ## (This function is out of phase from the current time by 1 sample)    
    def standard2ndOrder(self, deltaX):
        
        self.secondOrder = (self.sample_history[self.WINDOW_LENGTH-3]-2*self.sample_history[self.WINDOW_LENGTH-2]+self.sample_history[self.WINDOW_LENGTH-1])/(math.pow(deltaX,2))
        
        #push every value to the left by one
        self.secondOrder_history[:] = self.secondOrder_history[1:]+[self.secondOrder_history[0]]
         
        #push the current average into the EMA history from the left
        self.secondOrder_history[self.SECOND_ORDER_LENGTH-1] = self.secondOrder
                              
        return self.secondOrder
        
    ## This function just calls all the previous functions. Might not be that useful.    
    def applyFilters(self,new_sample,deltaX):

        self.updateSampleHistory(new_sample)
        self.simpleMovingAverage()
        self.exponentialMovingAverage()
        self.savitzkyGolayFilter()
        self.lagrangeDerivative(deltaX)
        self.getSlope(deltaX)
        self.standard2ndOrder(deltaX)

