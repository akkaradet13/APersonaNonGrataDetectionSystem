from flask import Flask
import RPi.GPIO as GPIO
import time, os
from playsound import playsound
from flask_http_response import success, result, error

app = Flask(__name__)

def relay(gpioControl):
    channel = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    if gpioControl == 'HIGH':
        GPIO.output(channel, GPIO.HIGH)
        GPIO.cleanup()
    elif gpioControl == 'LOW':
        GPIO.output(channel, GPIO.LOW)
    '''time.sleep(1)
    GPIO.output(channel, GPIO.LOW)'''
    #playSound('preview.mp3')
    #time.sleep(3)

def playSound(file):
    os.system("mpg123 " + file)

@app.route('/')
def Home():
    return ("<h1>Hello World</h1>")

@app.route('/actionDoor/<string:value>')
def ActionDoor(value):
    if value == '0':
        relay('HIGH')
        #playSound('preview.mp3')
        #return 'open'
    elif value == '1':
        relay('LOW')
        #return 'close'
    f = open("./Actiondoor.txt", "w")
    f.write(value)
    f.close()

@app.route('/levelSecurity/<string:value>')
def SetLevelSecurity(value):
    # f = open("./LevelSecurity.txt", "r")
    # print(f.read())
    
    f = open("./LevelSecurity.txt", "w")
    f.write(value)
    f.close()
    return ("<h1>200</h1>")

@app.route('/getValue/<string:value>')
def GetValue(value):
    f = open(f'./{value}.txt', "r")
    value = f.read()
    print('value', value)
    f.close()
    return success.return_response(message=str(value), status=300)
    

if __name__== '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)