import requests
import schedule
import time


def sendData():
    url = 'http://192.168.1.40/getData'
    myobj = {
        'postName' : 'koko',
        'description' : '123456789',
        'time' : '16/8/2020:23:06'
             }
    file = {
        'upload_file': open('download.png','rb')
        }
    x = requests.post(url, data = myobj, files=file)
    print(x.text)
'''
schedule.every().day.at("01:00").do(sendData)

while True:
    schedule.run_pending()
    time.sleep(60)
    print('ddd')
    sendData()
'''

sendData()

