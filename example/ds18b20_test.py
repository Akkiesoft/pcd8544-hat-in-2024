# DS18B20温度センサーテスト
"""
Required libralies and font:
* adafruit_framebuf
* adafruit_pcd8544
* font5x8.bin
(if you using RPi SBC)
* w1thermsensor
(if you using with Pico)
* adafruit_onewire
* adafruit_ds18x20
"""

# Choose your environment:
# rpi: Raspberry Pi SBC
# uhp: Raspberry Pi Pico with uHAT Porter Pico
# uhp_r2: Raspberry Pi Pico with uHAT Porter Pico Rev.2
from config import pcd8544_config
config = pcd8544_config("rpi")

import time
from digitalio import DigitalInOut, Direction, Pull
from busio import SPI
import adafruit_pcd8544

# DS18B20
if config.mode != "rpi":
    from adafruit_onewire.bus import OneWireBus
    from adafruit_ds18x20 import DS18X20
    onewire = OneWireBus(config.int_pin)
    ds18b20 = DS18X20(onewire, onewire.scan()[0])
else:
    from w1thermsensor import W1ThermSensor
    try:
        ds18b20 = W1ThermSensor()
    except:
        ds18b20 = False

# 令和6年最新版 PCD8544 HAT
spi = SPI(clock=config.sck, MOSI=config.mosi)
dc = DigitalInOut(config.dc)
cs = DigitalInOut(config.cs)
reset = DigitalInOut(config.rst)
display = adafruit_pcd8544.PCD8544(spi, dc, cs, reset)
display.bias = 4
display.contrast = 60
display.fill(0)
display.show()

# Switch on backlight
backlight = DigitalInOut(config.light)
backlight.direction = Direction.OUTPUT
backlight.value = 1

def get_temp():
    if config.mode != "rpi":
        return ds18b20.temperature
    else:
        return ds18b20.get_temperature() if ds18b20 else 0

try:
    while True:
        temperature = get_temp()
        display.fill_rect(24, 24, 36, 8, 0)
        display.text("Temperature", 10, 8, 1)
        display.text("{0:0.2f}C".format(temperature), 24, 24, 1)
        display.show()
        time.sleep(5)
finally:
    # clean display, turn off the backlight
    backlight.value = 0
    display.fill(0)
    display.show()
