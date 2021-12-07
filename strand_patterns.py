import time
import board
import neopixel
import random
import math
import threading
import psutil
import datetime


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

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

class Show:
    def __init__(self, lights, slider_size, slider_delay):
        self.num_pixels = lights
        self.slider_size = slider_size
        self.slider_delay = slider_delay
        self.thread = threading.Thread(target=self.run)
        self.isRed = True
        # computed properties
        self.slider_begin_extended_delay = int(math.ceil(lights / 3))
        self.slider_end_extended_delay = lights / 5
        # neopixel specific properties
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(pixel_pin, self.num_pixels, brightness=0.9, auto_write=False, pixel_order=self.ORDER)

    def start(self):
        #self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.thread.stop()

    # the show
    def run(self):
        while True:
            if not is_showtime():
                self.clear_all()
                time.sleep(60 * 15)
                continue


            for color in primary_colors:
                self.electric_slide_stacking(self.num_pixels, color, self.slider_size, False)
                time.sleep(3)
            self.electric_slide_stacking(self.num_pixels, random_color(), self.slider_size, True)
            time.sleep(3)
            self.inverted_electric_slide_stacking(self.num_pixels, random_color(), self.slider_size, True)
            time.sleep(3)
            for color in primary_colors:
                self.inverted_electric_slide_stacking(self.num_pixels, color, self.slider_size, False)
                time.sleep(3)
            #self.rainbow_cycle(0.009)
            #time.sleep(.5)


    def calc_slider_delay(self, i):
        if i < self.slider_end_extended_delay:
            time.sleep(self.slider_delay * 4)
        elif i < self.slider_begin_extended_delay:
            time.sleep(self.slider_delay * 3)
        else:
            time.sleep(self.slider_delay)

    

    def wheel(self, pos):
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
        return (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def candy_cane(self):
        for i in range(self.num_pixels):
            if i % 5 == 0:
                self.isRed = not self.isRed
            if self.isRed:
                self.pixels[i] = (0, 255, 0)
            else:
                self.pixels[i] = (255, 255, 255)
        self.pixels.show()
        time.sleep(.4)
        self.isRed = not self.isRed

    def electric_slide(self):
        for i in range(self.num_pixels):
            print("I", i)
            if i != 0:
                self.clear_previous_left(i)
            self.pixels[i] = self.wheel(i & 255)
            self.pixels.show()
            time.sleep(.009)

    def electric_slide_stacking(self, pxls, color, count, useRandom):
        print("FIRED", pxls)
        for i in range(0, pxls, count):
            if i != 0:
                self.clear_previous_left(i)
            self.pixels[i] = color
            if i + count == pxls:
                for x in range(count):
                    self.pixels[i + x] = color
                self.pixels.show()
                if useRandom is True:
                    color = random_color()
                self.electric_slide_stacking(pxls - count, color, count, useRandom)
                break
            for y in range(count):
                self.pixels[i + y] = color
            self.pixels.show()
            self.calc_slider_delay(pxls)

    def inverted_electric_slide(self, pxls, color, count):
        for i in range(pxls - 1, -1, count * -1):
            if i != self.num_pixels - 1:
                self.clear_previous_right(pxls, i)
            for y in range(count):
                self.pixels[i - y] = color 
            self.pixels.show()

    def inverted_electric_slide_stacking(self, pxls, color, count, useRandom):
        # 300 - 300 - 1 = -1
        # 300 - 290 - 1 = 9
        # 300 - 280 - 1 = 19
        head = self.num_pixels - pxls - 1
        for i in range(self.num_pixels - 1, head, count * -1):
            if i != self.num_pixels -1:
                self.clear_previous_right(i)
            if i - count == head:
                for x in range(count):
                    self.pixels[i - x] = color
                self.pixels.show()
                if useRandom is True:
                    color = random_color()
                self.inverted_electric_slide_stacking(pxls - count, color, count, useRandom)
                break
            for y in range(count):
                self.pixels[i - y] = color
            self.pixels.show()
            self.calc_slider_delay(pxls)

    def clear_all(self):
        self.pixels.fill(off)
        self.pixels.show()

    def clear_previous_right(self, i):
        for pxl in range(self.num_pixels - 1, i, -1):
            self.pixels[pxl] = off

    def clear_previous_left(self, i):
        for pxl in range(i):
            self.pixels[pxl] = off

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # TODO add a check if black
    return (g, r, b)

def is_showtime():
    start = datetime.time(18, 0, 0)
    end = datetime.time(23, 55, 0)
    current = datetime.datetime.now().time()
    return start <= current <= end


def execute_app():
    while True:
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
        for _ in range(60):
            rainbow_cycle(.009)


def handle_cleanup():
    pixels.deinit()

def main():
    try:
        execute_app()
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()
