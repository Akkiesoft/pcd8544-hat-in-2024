# Draw graph, data from Zabbix

"""
Required libralies and font:
* adafruit_framebuf
* adafruit_pcd8544
* font5x8.bin
"""

# Choose revision if you are using uHAT Porter Pico
#import uhat_porter_pico_type_p as board_bcm
import uhat_porter_pico_type_p3 as board_bcm

import board
from digitalio import DigitalInOut, Direction, Pull
import time
import json
# display
from busio import SPI
import adafruit_pcd8544
# network
from akkie_wifi import akkie_wifi
from akkie_wifi_config import ap_list
import adafruit_requests

# my own libraries and images
from draw_graph import draw_graph

zbx_url   = "http://192.168.x.x/api_jsonrpc.php"
zbx_token = ""
zbx_item  = 

# Display setup
spi = SPI(clock=board_bcm.BCM11, MOSI=board_bcm.BCM10)
dc = DigitalInOut(board_bcm.BCM25)
cs = DigitalInOut(board_bcm.BCM8)
reset = DigitalInOut(board_bcm.BCM24)

display = adafruit_pcd8544.PCD8544(spi, dc, cs, reset)
display.bias = 4
display.contrast = 60
display.fill(0)
display.show()

# Switch on backlight
backlight = DigitalInOut(board_bcm.BCM23)
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
        wifi.connect()
        data = get_zabbix_item(zbx_url, zbx_token, [zbx_item])
        last_clock = int(data['result'][0]['lastclock'])
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

btn = DigitalInOut(board_bcm.BCM27)
btn.switch_to_input(pull=Pull.UP)
btn_pressed = False

c = 0
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