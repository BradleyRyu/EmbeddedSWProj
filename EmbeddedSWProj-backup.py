import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont, ImageChops
import adafruit_rgb_display.st7789 as st7789

# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for color.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

# Loading display.
doraemon_pic = Image.open("bamboo_dor.png")
doraemon_pic = doraemon_pic.resize((width, height))
disp.image(doraemon_pic)
time.sleep(1)
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
draw.text((-1, 100), "[[GAME START]]", font=fnt, fill=rcolor)
disp.image(image)
time.sleep(2)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
disp.image(image)

dor_loc_x = 120
dor_loc_y = 120

def Up(y):
    if y <= -20:
       y = -20
    else:
        global dor_loc_y
        dor_loc_y -= 5
        y -= 5
    return y

def Down(y):
    if y >= 220:
        y = 220
    else:
        global dor_loc_y
        dor_loc_y += 5
        y += 5
    return y

def Left(x):
    if x <= -20:
        x = -20
    else:
        global dor_loc_x
        dor_loc_x -= 5
        x -= 5
    return x

def Right(x):
    if x >= 220:
        x = 220
    else:
        global dor_loc_x
        dor_loc_x += 5
        x += 5
    return x
    
def Doraemon(x_dor, y_dor):
    draw.ellipse((x_dor - 20, y_dor - 20, x_dor + 20, y_dor + 20), outline=(0, 0, 0), fill=(70, 161, 222))
    

while True:
    
    Doraemon(dor_loc_x, dor_loc_y)
    
    
    if not button_U.value:  # up pressed
        Doraemon(dor_loc_x, Up(dor_loc_y))
    
    if not button_D.value:  # down pressed
        Doraemon(dor_loc_x, Down(dor_loc_y))
    
    if not button_L.value:  # left pressed
        Doraemon(Left(dor_loc_x), dor_loc_y)

    if not button_R.value:  # right pressed
        Doraemon(Right(dor_loc_x), dor_loc_y)

    if not button_C.value:  # center pressed
        center_fill = button_fill
    
    if not button_A.value:  # left pressed
        new_color = (255, 0, 0)
    
    if not button_B.value:  # left pressed
        new_color = (0, 255, 0)
    
    
    # Display the Image
    
    disp.image(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    time.sleep(0.01)

