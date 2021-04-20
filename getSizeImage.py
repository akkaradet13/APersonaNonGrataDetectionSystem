import cv2
import os
import matplotlib.pyplot as plt
import matplotlib
from skin_seg import *
matplotlib.font_manager.fontManager.addfont('./Sarabun-Regular.ttf')
matplotlib.rc('font', family='Sarabun')
def plotSize(menu):
    dataPoints = []
    color = ['b','g','r','c','m','y','k','w']
    dataW = []
    dataH = []
    for m in menu:
        listDir = os.listdir(f'./dataSet3/croup/{m}/')
        Wdata = []
        Hdata = []
        for i in listDir:
            im = cv2.imread(f'./dataSet3/croup/{m}/{i}')
            h,w,c = im.shape
            Hdata.append(h)
            Wdata.append(w)
            dataH.append(h)
            dataW.append(w)
        dataPoints.append([Hdata,Wdata,m])
    print(f'Wmin{min(dataW)} Wmax{max(dataW)}')
    print(f'Hmin{min(dataH)} Hmax{max(dataH)}')
    
    for i,dataPoint in enumerate(dataPoints):
        plt.scatter(dataPoint[0], dataPoint[1], label=dataPoint[2] ,color=color[i], s=25,marker="o")
    plt.xlabel("H")
    plt.ylabel("W")
    plt.title('Size Image W H')
    plt.legend()
    plt.show()
    
def plotCountSkin(menu):
    dataPoints = []
    skin_detect = Skin_Detect()
    color = ['b','g','r','c','m','y','k','w']
    dataPixcelSkin = []
    for m in menu:
        listDir = os.listdir(f'./dataSet3/croup/{m}/')
        ypoints = []
        xpoints = np.arange(1,len(listDir)+1,1)
        for i in listDir:
            im = cv2.imread(f'./dataSet3/croup/{m}/{i}')
            skin_img = skin_detect.RGB_H_CbCr(im,False)
            # np.savetxt("foo.csv", skin_img, delimiter=",")
            
            P1 = np.count_nonzero(skin_img==1)
            # P0 = np.count_nonzero(skin_img==0)
            dataPixcelSkin.append(P1/100)
            ypoints.append(P1/100)
        dataPoints.append([xpoints,ypoints,m])
        # xpoints = np.arange(1,len(listDir)+1,1)
        # print(ypoints,xpoints)
        # plt.plot(xpoints, ypoints, 'o')
        # plt.show()
    print(f'mindataPixcelSkin {min(dataPixcelSkin)} maxdataPixcelSkin{max(dataPixcelSkin)}')
    
    for i,dataPoint in enumerate(dataPoints):
        plt.scatter(dataPoint[1], dataPoint[0], label=dataPoint[2] ,color=color[i], s=25,marker="o")
    plt.xlabel("quantity of pixcel skin")
    plt.ylabel("arange")
    plt.title('Size Image W H')
    plt.legend()
    plt.show()
            
menu = ['หน้าตรง', 'หน้ากาก', 'แว่น', 'แว่นดำ', 'แว่นหน้ากาก']
plotSize(menu)
plotCountSkin(menu)