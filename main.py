#import board
#import displayio
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import time
#from adafruit_bitmap_font import bitmap_font
from adafruit_magtag.magtag import MagTag
#from adafruit_display_shapes.line import Line

arial_font = "/fonts/Arial-12.bdf"

magtag = MagTag()
#display = board.DISPLAY
#splash = displayio.Group()
#display.show(splash)

# URLs to fetch from
PROD_URL = "http://homeassistant.localdomain:3123/api/taps"

deepSleepTime = 60*60;

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

#print("Available WiFi networks:")
#for network in wifi.radio.start_scanning_networks():
#    print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
#            network.rssi, network.channel))
#wifi.radio.stop_scanning_networks()

wifi.radio.connect(secrets["ssid"], secrets["password"])

#ipv4 = ipaddress.ip_address("8.8.4.4")
#print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

exceptionInfo = ""
json = None
strings = {}

try:
    response = requests.get(PROD_URL)
    json = response.json();
except BaseException as error:
    exceptionInfo = f"Error {error=}, {type(err)=}"
    # TODO: Load cached information

if json is None:
    magtag.add_text(
        text_position=(
            10,
            (magtag.graphics.display.height // 2) - 1,
        ),
        text_scale=1.5,
    )
    magtag.set_text("Unknown error, no JSON")
    magtag.exit_and_deep_sleep(deepSleepTime)

xSpacing = 6
ySpacing = 4
centreX = magtag.graphics.display.width // 2

#line = Line(x0 = centreX, y0 = ySpacing, x1 = centreX, y1 = magtag.graphics.display.height - ySpacing, color = None)
#splash.append(line)

# Tap names
strings["tap1label"] = magtag.add_text(
    text_font = arial_font,
    text_position=(
        centreX - xSpacing,
        ySpacing,
    ),
    text_anchor_point=(1,0),
    text_maxlen = 15,
    text_scale=1,
)

strings["tap2label"] = magtag.add_text(
    text_font = arial_font,
    text_position=(
        centreX + xSpacing,
        ySpacing,
    ),
    text_anchor_point=(0,0),
    text_maxlen = 15,
    text_scale=1,
)

strings["tap1name"] = magtag.add_text(
    text_font = arial_font,
    text_position=(
        xSpacing,
        (magtag.graphics.display.height//5) * 1,
    ),
    text_anchor_point=(0,0),
    text_maxlen = 25,
    text_scale=1,
)
strings["tap1style"] = magtag.add_text(
    text_font = arial_font,
    text_position=(
        xSpacing,
        (magtag.graphics.display.height//5) * 2,
    ),
    text_anchor_point=(0,0),
    text_maxlen = 25,
    text_scale=1.25,
)
strings["tap1abv"] = magtag.add_text(
#    text_font = arial_font,
    text_position=(
        xSpacing,
        (magtag.graphics.display.height//5) * 3,
    ),
    text_anchor_point=(0,0),
    text_maxlen = 15,
    text_scale=1,
)

strings["tap1ibu"] = magtag.add_text(
#    text_font = arial_font,
    text_position=(
        centreX - xSpacing,
        (magtag.graphics.display.height//5) * 3,
    ),
    text_anchor_point=(1,0),
    text_maxlen = 15,
    text_scale=1,
)

strings["tap2name"] = magtag.add_text(
    text_font = arial_font,
    text_position=(
        (magtag.graphics.display.width) - xSpacing,
        (magtag.graphics.display.height//5) * 1,
    ),
    text_anchor_point=(1,0),
    text_maxlen = 25,
    text_scale=1,
)
strings["tap2style"] = magtag.add_text(
    text_font = arial_font,
    text_position=(
        (magtag.graphics.display.width) - xSpacing,
        (magtag.graphics.display.height//5) * 2,
    ),
    text_anchor_point=(1,0),
    text_maxlen = 25,
    text_scale=1.25,
)
strings["tap2abv"] = magtag.add_text(
#    text_font = arial_font,
    text_position=(
        (magtag.graphics.display.width) - xSpacing,
        (magtag.graphics.display.height//5) * 3,
    ),
    text_anchor_point=(1,0),
    text_maxlen = 15,
    text_scale=1,
)

strings["tap2ibu"] = magtag.add_text(
#    text_font = arial_font,
    text_position=(
        centreX + xSpacing,
        (magtag.graphics.display.height//5) * 3,
    ),
    text_anchor_point=(0,0),
    text_maxlen = 15,
    text_scale=1,
)


magtag.set_text(json["data"][0]["name"], strings["tap1label"], False)
magtag.set_text(json["data"][1]["name"], strings["tap2label"], False)
if json["data"][0]["beer"] is None:
    magtag.set_text("None :(", strings["tap1name"], False)
else:
    magtag.set_text(json["data"][0]["beer"]["name"], strings["tap1name"], False)
    magtag.set_text(json["data"][0]["beer"]["style"], strings["tap1style"], False)
    magtag.set_text("ABV: %s" % json["data"][0]["beer"]["abv"], strings["tap1abv"], False)
    magtag.set_text("IBU: %s" % json["data"][0]["beer"]["ibu"], strings["tap1ibu"], False)

if json["data"][1]["beer"] is None:
    magtag.set_text("None :(", strings["tap2name"], False)
else:
    magtag.set_text(json["data"][1]["beer"]["name"], strings["tap2name"], False)
    magtag.set_text(json["data"][1]["beer"]["style"], strings["tap2style"], False)
    magtag.set_text("ABV: %s" % json["data"][1]["beer"]["abv"], strings["tap2abv"], False)
    magtag.set_text("IBU: %s" % json["data"][1]["beer"]["ibu"], strings["tap2ibu"], False)

time.sleep(2)


magtag.refresh()
magtag.exit_and_deep_sleep(deepSleepTime)

