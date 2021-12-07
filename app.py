from dotenv import load_dotenv
import os
import sys
from strand_patterns import Show

load_dotenv()

LIGHTS = int(os.getenv('LIGHTS'))
SLIDER_SIZE = int(os.getenv('SLIDER_SIZE'))
SLIDER_DELAY = float(os.getenv('SLIDER_DELAY'))

        



if __name__ == '__main__':
    show.start()
    
