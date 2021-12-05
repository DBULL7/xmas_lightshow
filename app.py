from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import sys
from strand_patterns import Show

load_dotenv()

LIGHTS = int(os.getenv('LIGHTS'))
SLIDER_SIZE = int(os.getenv('SLIDER_SIZE'))
SLIDER_DELAY = float(os.getenv('SLIDER_DELAY'))

if LIGHTS == None or SLIDER_SIZE == None or SLIDER_DELAY == None:
    sys.exit("ENV VAR NOT SET")
        
show = Show(LIGHTS, SLIDER_SIZE, SLIDER_DELAY)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('lights')  # access the data inside 
        slider = request.form.get('slider')
        slider_delay = request.form.get('slider-delay')
        print("lights", username, "slider", slider, "SLIDER_DELAY", slider_delay)


    return render_template('env.html', lights=LIGHTS, slider_size=SLIDER_SIZE, slider_delay=SLIDER_DELAY)

if __name__ == '__main__':
    show.start()
    app.run(debug=True, host='0.0.0.0')
    
