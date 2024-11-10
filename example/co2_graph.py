# Draw graph, data from Zabbix

"""
Required libralies and font:
* adafruit_framebuf
* adafruit_pcd8544
* font5x8.bin
* adafruit_requests or requests
"""

# Choose your environment:
# rpi: Raspberry Pi SBC
# uhp: Raspberry Pi Pico with uHAT Porter Pico
# uhp_r2: Raspberry Pi Pico with uHAT Porter Pico Rev.2
from config import pcd8544_config
config = pcd8544_config("rpi")

import board
from digitalio import DigitalInOut, Direction, Pull
import time
import json
# display
from busio import SPI
import adafruit_pcd8544
# network
if config.mode != "rpi":
    from akkie_wifi import akkie_wifi
    from akkie_wifi_config import ap_list
    import adafruit_requests
else:
    import requests

# my own libraries and images
from lib.draw_graph import draw_graph

zbx_url   = "http://192.168.x.x/api_jsonrpc.php"
zbx_token = ""
zbx_item  =

# Display setup
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
backlight.value =1


zbx_headers = { "Content-Type": "application/json-rpc" }
def get_zabbix_history(url, token, items, limit):
    hour_ago = time.time() - limit * 60
    zbx_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "history": 0,
            "itemids": items,
            "sortfield": "clock",
            "sortorder": "DESC",
            "limit": limit
        },
        "id": 1,
        "auth": token
    })
    with requests.post(url, headers = zbx_headers, data = zbx_request) as r:
        result = r.json()
    return result

def get_zabbix_item(url, token, items):
    zbx_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": { "itemids": items },
        "id": 1,
        "auth": token
    })
    with requests.post(url, headers = zbx_headers, data = zbx_request) as r:
        result = r.json()
    return result

latest_clock = 0
def update_graph():
    global latest_clock
    try:
        if config.mode != "rpi":
            wifi.connect()
        data = get_zabbix_item(zbx_url, zbx_token, [zbx_item])
        last_clock = int(data['result'][0]['lastclock'])
        if config.mode != "rpi":
            wifi.disconnect()
    except:
        last_clock = 0
    if latest_clock < last_clock:
        latest_clock = last_clock
        value = data['result'][0]['lastvalue']
        graph.add_data(float(value))
        display.fill_rect(56, 0, 28, 8, 0)
        display.text("%4d" % int(value), 56, 0, 1)
        graph.draw_graph()

if config.mode != "rpi":
    wifi = akkie_wifi(ap_list)
    wifi.connect()
    requests = adafruit_requests.Session(wifi.pool, wifi.ssl_context)

graph = draw_graph(display, 25,10, 58,38, 1050, 400)
display.text("Room CO2", 0, 0, 1)
display.text("%4d" % graph.y_max, 0, 10, 1)
display.text("%4d" % graph.y_min, 0, 40, 1)
display.show()

try:
    data = get_zabbix_history(zbx_url, zbx_token, [zbx_item], graph.width)
    if config.mode != "rpi":
        wifi.disconnect()
except:
    pass

for i in reversed(data['result']):
    graph.add_data(float(i['value']))
    last_data = i
graph.draw_graph()
latest_clock = int(data['result'][0]['clock'])

display.text("%4d" % int(last_data['value']), 56, 0, 1)
display.show()

btn = DigitalInOut(config.buttons[0])
btn.switch_to_input(pull=Pull.UP)
btn_pressed = False

c = 0
try:
    while True:
        if not btn.value:
            if not btn_pressed:
                backlight.value = 1 - backlight.value
            btn_pressed = True
        else:
            btn_pressed = False
        c += 1
        if 60 < c:
            update_graph()
            c = 0
        time.sleep(1)
finally:
    # clean display, turn off the backlight
    backlight.value = 0
    display.fill(0)
    display.show()
