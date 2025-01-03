# Graph demo

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
config = pcd8544_config("uhp")

from digitalio import DigitalInOut, Direction
import time
import random
# display
from busio import SPI
import adafruit_pcd8544

# my own libraries and images
from lib.draw_graph import draw_graph

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


# デフォルトのデータ
data = [50, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 100, 80]

# グラフの作成    (         位置,  サイズ,最大最小値, データ)
graph = draw_graph(display, 20,15, 50,33, 45, 0, data)
graph.draw_graph()

# ラベル
display.text("Graph Sample", 6, 2, 1)
display.text(" 45", 0, 15, 1)
display.text("  0", 0, 40, 1)

display.show()

while True:
    # ランダムなデータを配列に追加
    data.append(random.randint(5, 45))
    # グラフサイズから溢れた古いデータは消す
    if 49 <= len(data):
        del data[0]
    # グラフを描画
    graph.draw_graph()
    time.sleep(0.1)