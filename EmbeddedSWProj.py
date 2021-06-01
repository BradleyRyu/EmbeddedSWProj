import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
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

# Clear display.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
disp.image(image)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"
button_fill = "#FF00FF"
button_outline = "#FFFFFF"

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

init_x = 100
init_y = 100

white = (255, 255, 255)


draw.text((init_x, init_y), "@", font=fnt, fill=white)
currentcolor = white

while True:
    up_fill = 0
    if not button_U.value:  # up pressed
        up_fill = udlr_fill
        init_y -= 5
        if init_y <= 0:
            init_y = 0
        draw.text((init_x, init_y), "@", font=fnt, fill=currentcolor)

    down_fill = 0
    if not button_D.value:  # down pressed
        down_fill = udlr_fill
        init_y += 5
        if init_y >= 200:
            init_y = 200
        draw.text((init_x, init_y), "@", font=fnt, fill=white)

    left_fill = 0
    if not button_L.value:  # left pressed
        left_fill = udlr_fill
        init_x -= 5
        if init_x <= 0:
            init_x = 0
        draw.text((init_x, init_y), "@", font=fnt, fill=white)

    right_fill = 0
    if not button_R.value:  # right pressed
        right_fill = udlr_fill
        init_x += 5
        if init_x >= 200:
            init_x = 200
        draw.text((init_x, init_y), "@", font=fnt, fill=white)

    center_fill = 0
    if not button_C.value:  # center pressed
        center_fill = button_fill
    

    A_fill = 0
    if not button_A.value:  # left pressed
        currentcolor = (255, 0, 0)
    

    B_fill = 0
    if not button_B.value:  # left pressed
        currentcolor = (0, 255, 0)
    
    
    # Display the Image
    disp.image(image)

    time.sleep(0.01)
    