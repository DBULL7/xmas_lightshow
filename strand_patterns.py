import time
import board
import neopixel
import random
import math


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18


# total number of NeoPixels on potentially multiple strands
num_pixels = 50

# electric slide size, use more for larger strands to not have it take forever 
slider_size = 1
slider_delay = 0.01
# used for when the slider is past the halfway point,
# if you don't increase the timeout it can have a weird effect on the remaining pixels
slider_begin_extended_delay = int(math.ceil(num_pixels / 3))
slider_end_extended_delay = num_pixels / 5 
print("SLIDER EXTENDED DELAY POINT", slider_begin_extended_delay, "SLIDER END EXTENDED DELAY POINT", slider_end_extended_delay)


# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.9, auto_write=False, pixel_order=ORDER)

def calc_slider_delay(i):
    if i < slider_end_extended_delay:
        time.sleep(slider_delay * 4)
    elif i < slider_begin_extended_delay:
        time.sleep(slider_delay * 3)
    else:
        time.sleep(slider_delay)

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
        calc_slider_delay(pxls)

def inverted_electric_slide(pxls, color, count):
    for i in range(pxls - 1, -1, count * -1):
        if i != num_pixels - 1:
            clear_previous_right(pxls, i)
        for y in range(count):
            pixels[i - y] = color 
        pixels.show()

def inverted_electric_slide_stacking(pxls, color, count, useRandom):
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
        calc_slider_delay(pxls)



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
        rainbow_cycle(0.009)  # rainbow cycle with 1ms delay per step
        electric_slide()
        for color in primary_colors:
            electric_slide_stacking(num_pixels, color, slider_size, False)
            time.sleep(3)
        electric_slide_stacking(num_pixels, random_color(), slider_size, True)
        time.sleep(3)
        inverted_electric_slide_stacking(num_pixels, random_color(), slider_size, True)
        time.sleep(3)
        for color in primary_colors:
            inverted_electric_slide_stacking(num_pixels, color, slider_size, False)
            time.sleep(3)


def handle_cleanup():
    pixels.deinit()

def main():
    try:
        execute_app()
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()
