# PCD8544テスト用スクリプト

"""
Required libralies and font:
* adafruit_framebuf
* adafruit_pcd8544
* font5x8.bin
"""

# Choose your environment:
# rpi: Raspberry Pi SBC
# uhp: Raspberry Pi Pico with uHAT Porter Pico
# uhp_r2: Raspberry Pi Pico with uHAT Porter Pico Rev.2
from config import pcd8544_config
config = pcd8544_config("rpi")


from digitalio import DigitalInOut, Direction, Pull
import time
# display
from busio import SPI
import adafruit_pcd8544

# my own libraries and images
from lib.draw_img import draw_img
from lib.draw_graph import draw_graph
from imgs.uiiin import img_uiiin
from imgs.miku import img_miku

dummy_graph_data = (
    623, 625, 630, 632, 639, 643, 645, 646, 641, 615, 583, 556, 534, 524, 516, 508, 503, 498, 491, 483,
    483, 484, 487, 482, 477, 481, 478, 485, 482, 478, 476, 473, 464, 461, 456, 457, 459, 458, 460, 455,
    454, 446, 456, 449, 445, 443, 439, 437, 438, 442, 441, 444, 445, 449, 447, 452, 455, 458, 464, 471)

# Buttons
buttons = []
for b in config.buttons:
    buttons.append(DigitalInOut(b))
    buttons[-1].switch_to_input(pull=Pull.UP)
pressed = [False, False, False, False]

# Display setup

# 中華ボード(RPiの時のGPIO番号)
#spi = SPI(clock=board.GP2, MOSI=board.GP3) # Clock:BCM17, MOSI:BCM18
#dc = DigitalInOut(board.GP9)               # data/command:BCM27
#cs = DigitalInOut(board.GP8)               # Chip select:BCM22
#reset = DigitalInOut(board.GP7)            # Reset:BCM23

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

def img_with_speed(img, x = 0, y = 0):
    display.fill(0)
    a = time.monotonic_ns()
    draw_img(display, img, x, y)
    b = time.monotonic_ns()
    speed = "%.2f ms"%((b-a)/1000/1000)
    display.text(speed, 0, 0, 1)
    display.show()

def button_cmd(i):
    if i == 0:
        backlight.value = 1 - backlight.value
    elif i == 1:
        display.fill(0)
        graph = draw_graph(display, 25,10, 58,38, 800, 400)
        for i in dummy_graph_data:
            graph.add_data(i)
            last_data = i
        display.text("Room CO2", 0, 0, 1)
        display.text("%4d" % graph.y_max, 0, 10, 1)
        display.text("%4d" % graph.y_min, 0, 40, 1)
        graph.draw_graph()
    elif i == 2:
        img_with_speed(img_uiiin, 0, 16)
    elif i == 3:
        img_with_speed(img_miku, 0, 0)

img_with_speed(img_uiiin, 0, 16)

try:
    while True:
        for i in range(0, 4):
            if not buttons[i].value:
                if not pressed[i]:
                    button_cmd(i)
                pressed[i] = True
            else:
                pressed[i] = False
finally:
    # clean display, turn off the backlight
    backlight.value = 0
    display.fill(0)
    display.show()