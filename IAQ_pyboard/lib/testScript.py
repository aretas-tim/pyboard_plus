from ADS1115_pyboard_plus import ADS1115
from analog_sensor import Analog_Sensor


CO = Analog_Sensor('Mocon VOC',1)
print(CO.name)