import time
import machine
import neopixel
from umqtt.simple import MQTTClient

button = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
pixelpin = machine.Pin(4, machine.Pin.OUT)
np = neopixel.NeoPixel(pixelpin, 7, 3)
n = np.n
cheervalue = ""

# np animation parameters
total_steps = 255  # total number of steps in the pattern
step_index = 0  # current step within the pattern

# mqtt adafruit io variables

my_ornament = machine.unique_id()
mqtt_client = "rnMqttClient"
ada_url = "io.adafruit.com"
username = "rickardn"
ada_io_key = "7ae1640893fa401e941e71f726ffc72c"
c = MQTTClient(mqtt_client, ada_url, 0, username, ada_io_key)

def increment():  # increment the step_index
    global step_index
    global total_steps
    if step_index >= total_steps:
        step_index = 0
    else:
        step_index = step_index + 1


def wheel(wheel_pos):
    wheel_pos = 255 - wheel_pos
    if wheel_pos < 85:  # ( 0 - 255, 0, 252 - 0)  Spectrum  Red to
        # color = (255 - wheel_pos * 3, 0, round(wheel_pos * 2.2), 0)
        color = (75, 0, 0, 0)
        return color
    elif wheel_pos < 170:
        wheel_pos -= 85
        # color = (0, wheel_pos * 3, 255 - wheel_pos * 3, 0)
        color = (0, 0, 75, 0)
        return color
    else:
        wheel_pos -= 170
        # color = (wheel_pos * 3, 255 - wheel_pos * 3, 0, 0)
        color = (0, 75, 0, 0)
        return color


def rainbow_cycle():  # rainbow cycle animation
    for i in range(n):
        global step_index
        # rewrites each pixel in the ring using 1 of 3 color spectrum from the wheel function
        # each time the function is run the step_index is ++ 1
        # the order of pixels are constant 1   2   3   4   5   6  ...   16
        # wheel values on step_index 0 are 0, 16, 32, 48, 64, 80, ..., 240
        # wheel values on step_index 2 are 1, 17, 33, 49, 65, 81, ..., 241
        # Pixel color is moved to the next spectrum in wheel when the wheel function\
        # when the wheel value exceeds the spectrum step_index max value
        set_pixel_color = wheel(int((i * 256 / n) + step_index) & 255)
        np[i] = set_pixel_color
        np.write()
        increment()


def cheerwrite():
    c.connect()
    c.publish("rickardn/feeds/ornament.cheer", str(my_ornament))
    time.sleep(1)
    c.disconnect()

def cheercheck():
    c.connect()
    c.subscribe("rickardn/feeds/ornament.cheer")


# message for no holiday cheer available
# use x increment value of 3 for this function

def fade():
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

while True:
    x=0
    if not button.value():
        cheercheck()
        while x<150:
            rainbow_cycle()
            x += 1
            time.sleep(0.01)
        cheerwrite()

    # turn off the lights
    for i in range(n):
        np[i] = (0, 0, 0, 0)
        np.write()
        time.sleep_ms(45)