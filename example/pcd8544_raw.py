# PCD8544 SPIコマンドの練習用スクリプト

# Choose your environment:
# rpi: Raspberry Pi SBC
# uhp: Raspberry Pi Pico with uHAT Porter Pico
# uhp_r2: Raspberry Pi Pico with uHAT Porter Pico Rev.2
from config import pcd8544_config
config = pcd8544_config("uhp")

from digitalio import DigitalInOut, Direction, Pull
import time
# display
from busio import SPI
# image
from imgs.miku import img_miku

# Buttons
buttons = []
for b in config.buttons:
    buttons.append(DigitalInOut(b))
    buttons[-1].switch_to_input(pull=Pull.UP)
pressed = [False, False, False, False]

# 令和6年最新版 PCD8544 HAT
spi = SPI(clock=config.sck, MOSI=config.mosi)
dc = DigitalInOut(config.dc)
cs = DigitalInOut(config.cs)
reset = DigitalInOut(config.rst)

# Switch on backlight
backlight = DigitalInOut(config.light)
backlight.direction = Direction.OUTPUT
backlight.value = 1

# DCピントリセットピンを初期状態にする
dc.switch_to_output(value = False)
reset.switch_to_output(value = True)

# リセット
reset.value = False
time.sleep(0.1)
reset.value = True
time.sleep(0.1)

# SPIをロックする
spi.try_lock()

# 拡張設定モード
spi.write(bytearray([0x21]))
# バイアスを4に設定
spi.write(bytearray([0x10 | 0x04]))
# コントラストを60(0c3c)に設定
spi.write(bytearray([0x80 | 0x3c]))
# 通常設定モード
spi.write(bytearray([0x20]))

# 表示モードを通常モードにする
spi.write(bytearray([0x0c]))

# 描画座標を(0, 0)にセット
spi.write(bytearray([0x80 | 0x00]))
spi.write(bytearray([0x40 | 0x00]))

# DCピンをHIGHにしてデータの書き込みを開始
dc.value = True

# 画像データの配列でループ
for b in img_miku:
    spi.write(bytearray([b]))

# DCピンをHIGHにしてデータの書き込みを終了
dc.value = False

# 表示モードを反転モードにする
time.sleep(3)
spi.write(bytearray([0x0d]))

# 表示モードをブランクモードにする
time.sleep(3)
spi.write(bytearray([0x08]))

# 表示モードを通常モードにする
time.sleep(3)
spi.write(bytearray([0x0c]))

# 描画座標を(3, 8)にセット
spi.write(bytearray([0x80 | 0x03]))
spi.write(bytearray([0x40 | 0x01]))

# 各データの表示のされ方をテスト
dc.value = True
spi.write(bytearray([0x01]))
spi.write(bytearray([0x00]))
spi.write(bytearray([0x02]))
spi.write(bytearray([0x00]))
spi.write(bytearray([0x04]))
spi.write(bytearray([0x00]))
spi.write(bytearray([0x0f]))
spi.write(bytearray([0x00]))
spi.write(bytearray([0xff]))

# DCピンをHIGHにしてデータの書き込みを終了
dc.value = False

# 以下はGPIO27のボタン操作によるバックライトのオン・オフ切り替え用
def button_cmd(i):
    if i == 0:
        backlight.value = 1 - backlight.value
try:
    while True:
        for i in range(0, 4):
            if not buttons[i].value:
                if not pressed[i]:
                    button_cmd(i)
                pressed[i] = True
            else:
                pressed[i] = False
        time.sleep(0.01)
finally:
    # clean display, turn off the backlight
    backlight.value = 0
    display.fill(0)
    display.show()