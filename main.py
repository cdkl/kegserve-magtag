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
arial_bold_font = "/fonts/Arial_Bold_12.bdf"

magtag = MagTag()
#display = board.DISPLAY
#splash = displayio.Group()
#display.show(splash)

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# URLs to fetch from
PROD_URL = secrets["kegserve_url"] + "/api/v1/taps"

deepSleepTime = 60*60*24;

#print("Available WiFi networks:")
#for network in wifi.radio.start_scanning_networks():
#    print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
#            network.rssi, network.channel))
#wifi.radio.stop_scanning_networks()

json = None
status = None
strings = {}

try:
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    if not wifi.radio.connected:
        print("Failed to connect to WiFi.")
        raise RuntimeError("Failed to connect to WiFi.")

    wifi.radio.start_dhcp()
    # print("IP address: %s" % wifi.radio.ipv4_address)
    # print("DNS address: %s" % wifi.radio.dns)
    # print("Prod URL: %s" % PROD_URL)

    #ipv4 = ipaddress.ip_address("8.8.4.4")
    #print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

    pool = socketpool.SocketPool(wifi.radio)

    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    exceptionInfo = ""


    response = requests.get(PROD_URL)
    json = response.json()
    status = response.status_code
except Exception as e:
    exceptionInfo = str(e)
    print("Exception: %s" % exceptionInfo)
    magtag.set_text(f"Exception: {exceptionInfo}", auto_refresh=False)
    magtag.exit_and_deep_sleep(600)

if json is None:
    t = magtag.add_text(
        text_position=(
            (magtag.graphics.display.width // 2),
            (magtag.graphics.display.height // 2) - 10,
        ),
        line_spacing=0.75,
        text_wrap=42,
        text_anchor_point=(0.5, 0.5),  # center the text on x & y
    )
    magtag.set_text(f"Unknown error, no JSON from {PROD_URL} - ret {status}")
    magtag.exit_and_deep_sleep(600)

print("JSON: %s" % json)

xSpacing = 6
ySpacing = 4
centreX = magtag.graphics.display.width // 2

#line = Line(x0 = centreX, y0 = ySpacing, x1 = centreX, y1 = magtag.graphics.display.height - ySpacing, color = None)
#splash.append(line)

# # Tap names
# strings["tap1label"] = magtag.add_text(
#     text_font = arial_font,
#     text_position=(
#         centreX - xSpacing,
#         ySpacing,
#     ),
#     text_anchor_point=(1,0),
#     text_maxlen = 15,
#     text_scale=1,
# )

# strings["tap2label"] = magtag.add_text(
#     text_font = arial_font,
#     text_position=(
#         centreX + xSpacing,
#         ySpacing,
#     ),
#     text_anchor_point=(0,0),
#     text_maxlen = 15,
#     text_scale=1,
# )

name_scale = 1
style_scale = 1
abv_and_ibu_scale = 0.6

strings["tap1name"] = magtag.add_text(
    text_font = arial_bold_font,
    text_position=(
        xSpacing,
        (magtag.graphics.display.height//5) * 0 + ySpacing,
    ),
    text_anchor_point=(0,1),
    text_maxlen = 25,
    text_scale=name_scale,
)
strings["tap1style"] = magtag.add_text(
    text_font = arial_font,
    text_position=(
        xSpacing,
        (magtag.graphics.display.height//5) * 1 + ySpacing,
    ),
    text_anchor_point=(0,1),
    text_maxlen = 25,
    text_scale=style_scale,
)
strings["tap1abv_and_ibu"] = magtag.add_text(
#
    text_position=(
        xSpacing,
        (magtag.graphics.display.height//5) * 2 + ySpacing,
    ),
    text_anchor_point=(0,1),
    text_maxlen = 30,
    text_scale=abv_and_ibu_scale,
)

strings["tap3name"] = magtag.add_text(
    text_font = arial_bold_font,
    text_position=(
        (magtag.graphics.display.width) - xSpacing,
        (magtag.graphics.display.height//5) * 0 + ySpacing,
    ),
    text_anchor_point=(1,1),
    text_maxlen = 25,
    text_scale=name_scale,
)
strings["tap3style"] = magtag.add_text(
    text_font = arial_font,
    text_position=(
        (magtag.graphics.display.width) - xSpacing,
        (magtag.graphics.display.height//5) * 1 + ySpacing,
    ),
    text_anchor_point=(1,1),
    text_maxlen = 25,
    text_scale=style_scale,
)

strings["tap3abv_and_ibu"] = magtag.add_text(
    text_position=(
        (magtag.graphics.display.width) - xSpacing,
        (magtag.graphics.display.height//5) * 2 + ySpacing,
    ),
    text_anchor_point=(1,1),
    text_maxlen = 30,
    text_scale=abv_and_ibu_scale,
)

# Add tap 2 text displays (center-aligned, from bottom)
strings["tap2name"] = magtag.add_text(
    text_font = arial_bold_font,
    text_position=(
        magtag.graphics.display.width // 2,
        magtag.graphics.display.height - ((magtag.graphics.display.height//5) * 2 + ySpacing),
    ),
    text_anchor_point=(0.5,1),
    text_maxlen = 25,
    text_scale=name_scale,
)

strings["tap2style"] = magtag.add_text(
    text_font = arial_font,
    text_position=(
        magtag.graphics.display.width // 2,
        magtag.graphics.display.height - ((magtag.graphics.display.height//5) * 1 + ySpacing),
    ),
    text_anchor_point=(0.5,1),
    text_maxlen = 25,
    text_scale=style_scale,
)

strings["tap2abv_and_ibu"] = magtag.add_text(
    text_position=(
        magtag.graphics.display.width // 2,
        magtag.graphics.display.height - ySpacing,
    ),
    text_anchor_point=(0.5,1),
    text_maxlen = 30,
    text_scale=abv_and_ibu_scale,
)


# magtag.set_text(json[0]["name"], strings["tap1label"], False)
# magtag.set_text(json[1]["name"], strings["tap2label"], False)
if json[0]["beverage_id"] is None:
    magtag.set_text("None :(", strings["tap1name"], False)
else:
    magtag.set_text(json[0]["beverage"]["name"], strings["tap1name"], False)
    magtag.set_text(json[0]["beverage"]["style"], strings["tap1style"], False)
    magtag.set_text(f"ABV: {json[0]["beverage"]["abv"]} | IBU: {json[0]["beverage"]["ibu"]}", strings["tap1abv_and_ibu"], False)

if json[1]["beverage_id"] is None:
    magtag.set_text("None :(", strings["tap2name"], False)
else:
    magtag.set_text(json[1]["beverage"]["name"], strings["tap2name"], False)
    magtag.set_text(json[1]["beverage"]["style"], strings["tap2style"], False)
    magtag.set_text(f"ABV: {json[1]['beverage']['abv']} | IBU: {json[1]['beverage']['ibu']}", strings["tap2abv_and_ibu"], False)

if json[2]["beverage_id"] is None:
    magtag.set_text("None :(", strings["tap3name"], False)
else:
    magtag.set_text(json[2]["beverage"]["name"], strings["tap3name"], False)
    magtag.set_text(json[2]["beverage"]["style"], strings["tap3style"], False)
    magtag.set_text(f"ABV: {json[2]["beverage"]["abv"]} | IBU: {json[2]["beverage"]["ibu"]}", strings["tap3abv_and_ibu"], False)
 

# Add battery voltage display
strings["battery"] = magtag.add_text(
    text_position=(
        xSpacing,
        magtag.graphics.display.height - ySpacing,
    ),
    text_anchor_point=(0,1),
    text_maxlen = 10,
    text_scale=0.6,
)

# Set the battery voltage text with error handling
try:
    battery_voltage = magtag.peripherals.battery
    if battery_voltage is None:
        voltage_text = "?.??V"
    else:
        voltage_text = f"{float(battery_voltage):.2f}V"
except (ValueError, TypeError):
    voltage_text = "?.??V"

magtag.set_text(voltage_text, strings["battery"], False)

timestamp_label_spacing = 10

# Add timestamp display (2 lines in bottom right)
strings["timestamp_date"] = magtag.add_text(
    text_position=(
        magtag.graphics.display.width - xSpacing,
        magtag.graphics.display.height - ySpacing - timestamp_label_spacing,
    ),
    text_anchor_point=(1,1),
    text_maxlen = 10,
    text_scale=0.6,
)

strings["timestamp_time"] = magtag.add_text(
    text_position=(
        magtag.graphics.display.width - xSpacing,
        magtag.graphics.display.height - ySpacing,
    ),
    text_anchor_point=(1,1),
    text_maxlen = 10,
    text_scale=0.6,
)

TIME_URL = f"https://io.adafruit.com/api/v2/{secrets['adafruit_io_username']}/integrations/time/strftime?x-aio-key={secrets['adafruit_io_key']}&tz={secrets['timezone']}"
TIME_URL += "&fmt=%25Y-%25m-%25d+%25H:%25M:%25S"  # Simple format: YYYY-MM-DD HH:MM:SS
response = requests.get(TIME_URL)
print("Time response: %s" % response.text)

# Parse the time response manually
try:
    # Split date and time
    date_str, time_str = response.text.split(' ')
    year, month, day = [int(x) for x in date_str.split('-')]
    hour, minute, second = [int(x) for x in time_str.split(':')]
    
    # Create time_tuple (year, month, day, hour, minute, second, weekday, yearday, isdst)
    # We'll set weekday=0, yearday=1, and isdst=-1 as defaults
    current_time = time.struct_time((year, month, day, hour, minute, second, 0, 1, -1))
except (ValueError, TypeError):
    current_time = time.localtime()  # fallback to device time if parsing fails

# Set the timestamp texts
magtag.set_text(f"{current_time.tm_mday:02d}/{current_time.tm_mon:02d}", strings["timestamp_date"], False)
magtag.set_text(f"{current_time.tm_hour:02d}:{current_time.tm_min:02d}", strings["timestamp_time"], False)

time.sleep(2)


magtag.refresh()
magtag.exit_and_deep_sleep(deepSleepTime)

