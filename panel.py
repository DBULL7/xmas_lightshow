#!/usr/bin/env python3

import time
import sys
import displayio
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from logging import debug
import adafruit_imageload
import random
import string


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat' 
options.gpio_slowdown = 3
options.pixel_mapper_config = "V-mapper:Z"

matrix = RGBMatrix(options=options)

snowflake_height = 2
snowflake_width = 2
matrix_width = 64
matrix_height = 64

def create_snowflake(_x, _y):
    matrix.SetPixel(_x, _y, 255, 255, 255)
    matrix.SetPixel(_x +1, _y, 255, 255, 255)
    matrix.SetPixel(_x, _y + 1, 255, 255, 255)
    matrix.SetPixel(_x +1, _y + 1, 255, 255, 255)

def clear_row(_y):
    if _y == -2:
        return
    for i in range(matrix_width):
        matrix.SetPixel(i, _y, 0, 0, 0)
        matrix.SetPixel(i, _y + 1, 0, 0, 0)
    print("cleared row", _y)

def snow():
    offset = False
    while True:
        for y in range(0, 64, snowflake_height):
            clear_row(y -2)
            print("Y:", y)
            for x in range(0, 63, 8):
                if x % 2 == 0:
                    if not offset:
                        create_snowflake(x, y + 2) 
                    else:
                        create_snowflake(x, y + 4)

            clear_row(y + 2)
            offset = not offset
            time.sleep(.500)
        
        
def matrix_anim():
    for i in range(64):
        print(random.choice(string.ascii_letters))



def stack_anim():
    for y in range(32):
        for x in range(64):
            matrix.SetPixel(x, y, random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))
            time.sleep(.001)
    for _y in range(32, 64):
        for x in range(64):
            matrix.SetPixel(x, _y, 255, 0, 0)
            time.sleep(.001)
    time.sleep(3)

# group = displayio.Group()

#  load in party parrot bitmap
# parrot_bit, parrot_pal = adafruit_imageload.load("./partyParrotsTweet.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)

#parrot_grid = displayio.TileGrid(parrot_bit, pixel_shader=parrot_pal, width=1, height=1, tile_height=32, tile_width=32, default_tile=10, x=0, y=0)

# group.append(parrot_grid)

image = Image.open("./partyParrotsTweet.bmp")
#image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
print("SIZE", image.size)

w, h = image.size


try:
    print("Press CTRL-C to stop.")
    while True:
        for i in range(9):
            left = i * 32
            right = (i * 32) + 32
            img = image.crop((left, 0, right, 32))
            img = img.resize((64, 64), Image.ANTIALIAS)
            matrix.SetImage(img.convert('RGB'))
            time.sleep(.1)

        #matrix.SetImage(image.convert('RGB'))
        #matrix.SetPixel(1, 1, 255, 255, 255)
    #stack_anim()
    #snow()
    # matrix_anim() 

except KeyboardInterrupt:
    sys.exit(0)
