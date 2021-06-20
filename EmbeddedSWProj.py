"""
Question
bullet falls from the top and I have to move Doraemon.
however, i cannot move Doraemon until Laser arrives Bottom.
How can i move Doraemon independently?
"""




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
image = Image.new("RGBA", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

# Loading display.
doraemon_pic2 = Image.open("bamboo_dor.png")
doraemon_pic = doraemon_pic2.resize((width, height))
doraemon_character = doraemon_pic2.resize((50, 50))
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

#DORAEMON LOCATION
dor_loc_x = 120
dor_loc_y = 120

#init laser location
laser_loc_x = 120
laser_loc_y = 0


#ULTIMATE SKILL : defense all attacks
cool_time = 20

#score 
score = 0

def Doraemon(x_dor, y_dor, doraemon):
    # square of 40 
    #draw.rectangle((x_dor - 20, y_dor - 20, x_dor + 20, y_dor + 20), outline=(255, 255, 255), fill=(70, 161, 222))
    image.paste(doraemon, (x_dor - 20,y_dor - 20), doraemon)

def Draw_laser(laser_loc_x, laser_loc_y):
    
    top_x = laser_loc_x
    top_y = laser_loc_y
    left_x = laser_loc_x - 5
    bottom_y = laser_loc_y + 8.66
    right_x = laser_loc_x + 5
    
    draw.polygon([(top_x, top_y), (left_x, bottom_y), (right_x, bottom_y)],
                 outline=(random.randint(-100, 100) % 256, random.randint(-100, 100) % 256, random.randint(-100, 100) % 256),
                 fill=(255, 0, 0))
    
    
    # if bullet touches Doraemon
    
    if ((dor_loc_y - 20) - bottom_y <= 10) and (right_x > dor_loc_x - 20  or left_x < dor_loc_x + 20):
        for i in range(5):
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((45, 80), "|| JIN GU ||",font=fnt, fill=rcolor)
            disp.image(image)
            time.sleep(0.3)
            draw.text((30, 140),"||GOT YOU||", font=fnt, fill=rcolor)
            disp.image(image)
        time.sleep(2)
        exit()
    
def Laser(laser_loc_x, laser_loc_y):
    
    if laser_loc_y >= 240:
        laser_loc_x = random.randint(0, 240)
        laser_loc_y = 0
    
    #triangle coordinate
    top_x = laser_loc_x
    top_y = laser_loc_y
    left_x = laser_loc_x - 5
    bottom_y = laser_loc_y + 8.66
    right_x = laser_loc_x + 5
    
    draw.polygon([(top_x, top_y), (left_x, bottom_y), (right_x, bottom_y)],
                 outline=(random.randint(-100, 100) % 256, random.randint(-100, 100) % 256, random.randint(-100, 100) % 256),
                 fill=(255, 0, 0))
        
def Up(y):
    if y <= 30:
       y = 30
    else:
        global dor_loc_y
        dor_loc_y -= 5
        y -= 5
    return y

def Down(y):
    if y >= 210:
        y = 210
    else:
        global dor_loc_y
        dor_loc_y += 5
        y += 5
    return y

def Left(x):
    if x <= 30:
        x = 30
    else:
        global dor_loc_x
        dor_loc_x -= 5
        x -= 5
    return x

def Right(x):
    if x >= 210:
        x = 210
    else:
        global dor_loc_x
        dor_loc_x += 5
        x += 5
    return x
    


init_x = 100
init_y = 100
stage = 1


init_time = time.time()

while True:
    
    draw.text((0, 0), str(score), font=fnt, fill=(255, 255, 255))
    
    if score % 10 == 0 and score > 5:
        stage += 1
    
    
    if not button_U.value:  # up pressed
        Up(dor_loc_y)
    
    if not button_D.value:  # down pressed
        Down(dor_loc_y)
    
    if not button_L.value:  # left pressed
        Left(dor_loc_x)

    if not button_R.value:  # right pressed
        Right(dor_loc_x)
        
    if not button_C.value:  # center pressed
        center_fill = button_fill
    
    if not button_A.value:  # 5 pressed
        new_color = (255, 0, 0)
    
    
    if not button_B.value:  # 6 pressed
        new_color = (0, 255, 0)
    
    laser_loc_y += 10
    if laser_loc_y >= 240:
        laser_loc_x = random.randint(0, 240)
        laser_loc_y = 0
        score += 1
    
    Doraemon(dor_loc_x, dor_loc_y, doraemon_character)
    Laser(laser_loc_x, laser_loc_y)
    
    # Display the Image
    disp.image(image)
    
    # Clear Display
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    time.sleep(0.01)

