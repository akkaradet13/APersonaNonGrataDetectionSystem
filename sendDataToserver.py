import requests, schedule, os.path, time

def getFile():
    path = './dataset/'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
            print(r,d,file)
    
    return files

def CreateInfo(imgPath):
    nameIMG = os.path.basename(imgPath)
    timeIMG = time.ctime(os.path.getctime(imgPath))
    return [nameIMG,timeIMG]

def sendData():
    AllFile = getFile()
    for imgPath in AllFile:
        Info = CreateInfo(imgPath)
        url = 'http://192.168.1.45/getData'
        myobj = {
            'name' : Info[0],
            'time' : Info[1]
            }
        file = {
            'upload_file': open(imgPath,'rb')
            }
        x = requests.post(url, data = myobj, files=file)
        #x = requests.post(url, files=file)
    
'''
schedule.every().day.at("01:00").do(sendData)

while True:
    schedule.run_pending()
    time.sleep(60)
    print('ddd')
    sendData()
'''

getFile()
sendData()
print('200')
