# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 300

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.6, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

isRed = True

def candy_cane():
    global isRed
    for i in range(num_pixels):
        if i % 5 == 0:
            isRed = not isRed
        if isRed:
            pixels[i] = (0, 255, 0)
        else:
            pixels[i] = (255, 255, 255)
    pixels.show()
    time.sleep(.4)
    isRed = not isRed

def electric_slide():
    for i in range(num_pixels):
        if i != 0:
            clear_previous_left(i)
        pixels[i] = wheel(i & 255)
        pixels.show()
        time.sleep(.009)

def electric_slide_stacking(pxls, color, count, useRandom):
    print(pxls)
    for i in range(0, pxls, count):
        if i != 0:
            clear_previous_left(i)
        pixels[i] = color
        if i + count == pxls:
            for x in range(count):
                pixels[i + x] = color
            pixels.show()
            if useRandom is True:
                color = random_color()
            electric_slide_stacking(pxls - count, color, count, useRandom)
            break
        for y in range(count):
            pixels[i + y] = color
        pixels.show()
        # time.sleep(.009)

def inverted_electric_slide(pxls, color, count):
    print(pxls)
    for i in range(pxls - 1, -1, count * -1):
        print("HERE",i)
        if i != num_pixels - 1:
            clear_previous_right(pxls, i)
        #for y in range(count, 0, -1):
        for y in range(count):
            print("Y", i - y, i, y)
            pixels[i - y] = color 
        pixels.show()

def inverted_electric_slide_stacking(pxls, color, count, useRandom):
    print(pxls)
    # 300 - 300 - 1 = -1
    # 300 - 290 - 1 = 9
    # 300 - 280 - 1 = 19
    head = num_pixels - pxls - 1
    for i in range(num_pixels - 1, head, count * -1):
        if i != num_pixels -1:
            clear_previous_right(i)
        if i - count == head:
            for x in range(count):
                pixels[i - x] = color
            pixels.show()
            if useRandom is True:
                color = random_color()
            inverted_electric_slide_stacking(pxls - count, color, count, useRandom)
            break
        for y in range(count):
            pixels[i - y] = color
        pixels.show()



def clear_all(pxls):
    pixels.fill(off)
    pixels.show()

def clear_previous_right(i):
    for pxl in range(num_pixels - 1, i, -1):
        pixels[pxl] = off

def clear_previous_left(i):
    for pxl in range(i):
        pixels[pxl] = off

red = (0, 255, 0)
green = (255, 0, 0)
blue = (0, 0, 255)
purple = (0, 255, 255)
white = (255, 255, 255)
off = (0, 0, 0)


primary_colors = [
    red,
    green,
    blue,
    purple,
    white,
]

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # TODO add a check if black
    return (g, r, b)

def dance():
    offset = 3
    gap = False
    for pxl in range(0, num_pixels, offset): 
        if not gap:
            pixels[pxl] = blue
        else:
            pixels[pxl] = off
        if pxl % offset == 0:
            gap = not gap
    pixels.show()


def execute_app():
    while True:
        # rainbow_cycle(0.009)  # rainbow cycle with 1ms delay per step
        # electric_slide()
        # for color in primary_colors:
            # electric_slide_stacking(num_pixels, color, 10, False)
            # time.sleep(3)
        # time.sleep(3)
        # electric_slide_stacking(num_pixels, random_color(), 10, True)
        # time.sleep(3)
        # inverted_electric_slide_stacking(num_pixels, random_color(), 10, True)
        # time.sleep(3)
        # for color in primary_colors:
            # inverted_electric_slide_stacking(num_pixels, color, 10, False)
            # time.sleep(3)
        # pixels.fill((255, 0, 0))
        # pixels.show()
        # time.sleep(10)
        # candy_cane()
        dance()


def handle_cleanup():
    pixels.deinit()

def main():
    try:
        execute_app()
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()
