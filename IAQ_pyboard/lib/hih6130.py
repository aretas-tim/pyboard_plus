from pyb import I2C

class HIH6130:
    temp = 0
    rh = 0
    status = 0
    address = 0

    def __init__(self, address = 0x27):
        self.temp = 0
        self.rh = 0
        self.status = 0
        self.address = address

    def getTRH(self, i2c):

        data = bytearray(6)

        try:
            i2c.recv(data, self.address)
        except Exception as e:
            print(e)
            return -1

        Hum_H = data[0]
        Hum_L = data[1]
        Temp_H = data[2]
        Temp_L = data[3]

        status = (Hum_H >> 6) & 0x03
        Hum_H = Hum_H & 0x3f
        H_dat = ((Hum_H) << 8) | Hum_L
        T_dat = ((Temp_H) << 8) | Temp_L
        T_dat = T_dat / 4

        RH = H_dat * 6.10e-3
        TC = T_dat * 1.007e-2 - 40

        self.temp = TC
        self.rh = RH
        self.status = status
        return 0
