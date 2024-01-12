import spidev
from time import sleep

V_REF = 3.29476
CHN = 0

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def get_voltage():
    dout = spi.xfer2([((0b1000+CHN)>>2)+0b100,((0b1000+CHN)&0b0011)<<6,0])
    bit12 = ((dout[1]&0b1111) << 8) + dout[2]
    volts = round((bit12 * V_REF) / float(255),4)
    return volts

try:
    print('--- start program ---')
    while True:
        volts = get_voltage()
        print('volts= {:3.2f}'.format(volts))
        sleep(0.01)

except KeyboardInterrupt:
    pass
finally:
    spi.close()
    print('--- stop program ---')
