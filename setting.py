from flask import Flask
import RPi.GPIO as GPIO
import time, os
from playsound import playsound

app = Flask(__name__)

def relay():
    channel = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)

    GPIO.output(channel, GPIO.HIGH)
    '''time.sleep(1)
    GPIO.output(channel, GPIO.LOW)'''
    playSound('preview.mp3')
    #time.sleep(3)
    #GPIO.cleanup()

def playSound(file):
    os.system("mpg123 " + file)

@app.route('/')
def Home():
    return ("<h1>Hello World</h1>")

@app.route('/actionDoor/<string:value>')
def ActionDoor(value):
    if value == '0':
        relay()
        #playSound('preview.mp3')
        return 'open'
    elif value == '1':
        channel = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)
        GPIO.cleanup()
        return 'close'

if __name__== '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)