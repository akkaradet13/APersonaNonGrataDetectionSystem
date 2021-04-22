import requests, time, os

class PushData():
    host = 'http://192.168.1.45:70/getData'
    
    def __init__(self):
        entries = os.listdir('Data/')
        amountFile = len(entries)
        n = 0
        for file in entries:
            self.pushData(f'Data/{file}')
            time.sleep(1)
            n+=1
            print(f'Processing... {(amountFile/n)*100}%')
        print(entries)
        
    def pushData(self, file):
        # myobj = {
        #     'postName' : 'koko',
        #     'description' : '123456789',
        #     'time' : '16/8/2020:23:06'
        #          }
        file = {
            'upload_file': open(file,'rb')
            }
        # x = requests.post(url, data = myobj, files=file)
        x = requests.post(self.host, files=file)
        # if x.text == "200":
        #     os.remove(file)
        # else :
        #     print(f'Error {file}')
