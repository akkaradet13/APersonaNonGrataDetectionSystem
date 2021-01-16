import os

def checkFileName():
    n = 1
    entries = os.listdir('images')
    for i in entries:
        name = f'img{n}.jpg'
        if name in entries:
            n += 1
            print('ok')
        else:
            print(name)
            return name
checkFileName()