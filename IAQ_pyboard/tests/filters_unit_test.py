from filters import Filters

#create a filter object
test_obj = Filters()



##############################
# Test updateSampleHistory() #
##############################

# following loop should insert the current index into a list from the left
# and print to the screen the state of the moving window every loop iteration.
# Should print [0,1,2,3,4,5,6,7,8,9]
# for n in range(10):
#     test_obj.updateSampleHistory(n)
#     
# print("\nUpdat sample histpry test.\nShould print [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:")
# print(test_obj.sample_history)



################################
# Test simpleMovingAverage() 1 #
################################


# for n in range(10):
#     
#     #Load sample history with all n's
#     for t in range(10):
#         test_obj.updateSampleHistory(n)
#     
#     # take the simple moving average of the current sample frame 
#     # (each iteration the history is loaded) with all n's
#     test_obj.simpleMovingAverage()
#     
#     
# print("\nSimple Moving Average Test 1.\nShould print [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]:")
# print(test_obj.sma_history)


################################
# Test simpleMovingAverage() 2 #
################################

# #zero out the fields we are testing
# test_obj.sample_history = [0,0,0,0,0,0,0,0,0,0]
# test_obj.sma_history = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
# 
# #fake data samples with a spike at 8th indices
# data_samples = [1.1,1.3,1.6,1.5,1.3,1.1,1.1,5.0,1.4,1.3]
# 
# for i in range(10):
#     
#     test_obj.updateSampleHistory(data_samples[i])
#     print("\sample history:")
#     print(test_obj.sample_history)
#     test_obj.simpleMovingAverage()
#     print("\sma history:")
#     print(test_obj.sma_history)



##################################
# Test exponentialMovingAverage()#
##################################


# #zero out the fields we are testing
# test_obj.sample_history = [0,0,0,0,0,0,0,0,0,0]
# test_obj.ema_history = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
# 
# #fake data samples with a spike at 6/7th indices
# data_samples = [2.0,4.0,2.5,7.0,1.6,10.0,10.0,1.0,3.0,5.0]
# 
# for i in range(10):
#     
#     test_obj.updateSampleHistory(data_samples[i])
#     print("\sample history:")
#     print(test_obj.sample_history)
#     test_obj.exponentialMovingAverage()
#     print("\ema history:")
#     print(test_obj.ema_history)



##################################
# Test savitzkyGolayFilter()     #
##################################

#zero out the fields we are testing
# test_obj.sample_history = [0,0,0,0,0,0,0,0,0,0]
# test_obj.sga_values = [0.0,0.0,0.0,0.0,0.0]
# 
# #fake data samples 
# data_samples = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
# data_samples_2 = [1.0,2.0,1.0,2.0,1.0,2.0,1.0,2.0,1.0,2.0]
# data_samples_3 = [10.0,7.0,5.0,7.0,10.0,7.0,5.0,3.0,5.0,7.0]
# 
# for i in range(10):
#     
#     test_obj.updateSampleHistory(data_samples_3[i])
#     print("\sample history:")
#     print(test_obj.sample_history)
#     test_obj.savitzkyGolayFilter()
#     print("\sga values:")
#     print(test_obj.sga_values)
#     print("\sga history:")
#     print(test_obj.sga_history)




##################################
# Test lagrangeDerivative()      #
##################################

# #fake data samples
# data_samples_3 = [10.0,7.0,5.0,7.0,10.0,7.0,5.0,3.0,5.0,7.0]
# # a dummy time in milliseconds
# deltaX = 1000 
# 
# #zero out the fields we are testing
# test_obj.sample_history = [0,0,0,0,0,0,0,0,0,0]
# test_obj.lagrange_history = [0,0,0,0,0,0,0,0,0,0]
# 
# 
# for i in range(10):
#     
#     test_obj.updateSampleHistory(data_samples_3[i])
#     print("\sample history:")
#     print(test_obj.sample_history)
#     test_obj.lagrangeDerivative(deltaX)
#     print("\lagrange history:")
#     print(test_obj.lagrange_history)


##################################
#      Test getSlope()           #
##################################

# #fake data samples
# data_samples_3 = [10.0,7.0,5.0,7.0,10.0,7.0,5.0,3.0,5.0,7.0]
# # a dummy time in milliseconds
# deltaX = 1000 
# 
# #zero out the fields we are testing
# test_obj.sample_history = [0,0,0,0,0,0,0,0,0,0]
# test_obj.slope_history = [0,0,0,0,0,0,0,0,0,0]
# 
# 
# for i in range(10):
#     
#     test_obj.updateSampleHistory(data_samples_3[i])
#     print("\sample history:")
#     print(test_obj.sample_history)
#     test_obj.getSlope(deltaX)
#     print("\slope history:")
#     print(test_obj.slope_history)




##################################
#      Test standard2ndOrder()   #
##################################


# #fake data samples
# data_samples_4 = [10.0,9.0,7.0,4.0,5.0,5.5,5.0,3.0,6.0,10.0]
# # a dummy time in milliseconds
# deltaX = 1000 
# 
# #zero out the fields we are testing
# test_obj.sample_history = [0,0,0,0,0,0,0,0,0,0]
# test_obj.secondOrder_history = [0,0,0,0,0,0,0,0,0,0]
# 
# 
# for i in range(10):
#     
#     test_obj.updateSampleHistory(data_samples_4[i])
#     print("\sample history:")
#     print(test_obj.sample_history)
#     test_obj.standard2ndOrder(deltaX)
#     print("\slope history:")
#     print(test_obj.secondOrder_history)

data_samples_4 = [10.0,9.0,7.0,4.0,5.0,5.5,5.0,3.0,6.0,10.0]
deltaX = 1000 

for i in range(10):
    
    test_obj.updateSampleHistory(data_samples_4[i])
    
test_obj.applyFilters(deltaX)



