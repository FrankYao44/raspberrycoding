from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
 
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
 
with canvas(device) as draw:
    #draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((0, 0), "hello raspberry!", fill="white")
    draw.text((0,8),"hello raspberry!",fill="white")
