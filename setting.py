from flask import Flask
import RPi.GPIO as GPIO
import time, os
from playsound import playsound

app = Flask(__name__)

def relay(gpioControl):
    channel = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)

    GPIO.output(channel, GPIO.gpioControl)
    '''time.sleep(1)
    GPIO.output(channel, GPIO.LOW)'''
    playSound('preview.mp3')
    #time.sleep(3)
    GPIO.cleanup()

def playSound(file):
    os.system("mpg123 " + file)

@app.route('/')
def Home():
    return ("<h1>Hello World</h1>")

@app.route('/actionDoor/<string:value>')
def ActionDoor(value):
    if value == '0':
        relay(HIGH)
        #playSound('preview.mp3')
        return 'open'
    elif value == '1':
        relay(LOW)
        return 'close'

@app.route('/levelSecurity/<string:value>')
def SetLevelSecurity(value):
    # f = open("./LevelSecurity.txt", "r")
    # print(f.read())
    
    f = open("./LevelSecurity.txt", "w")
    f.write(value)
    f.close()
    return ("<h1>200</h1>")

@app.route('/getValue/<string:value>')
def GetValue(fileName):
    f = open(f'./{fileName}.txt', "r")
    value = f.read()
    f.close()
    return value
    

if __name__== '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)