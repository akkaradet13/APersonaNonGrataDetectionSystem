import matplotlib.pyplot as plt
import matplotlib
matplotlib.font_manager.fontManager.addfont('./Sarabun-Regular.ttf')
matplotlib.rc('font', family='Sarabun')
x = range(1970,2011,5)
take = [35017,36273,36895,36286,34771,33451,31935,30657,28655]
ono = [183325,185503,180901,177532,166930,159890,155200,150225,145217]
fuku = [355264,405677,425675,441502,445403,453791,456908,459087,459087]
ax = plt.gca()
ax.set_title(u'ประชากรในช่วง 40 ปี',fontname='Tahoma',fontsize=13)
ax.set_xlabel(u'ปี (ค.ศ.)',fontname='Tahoma',fontsize=13)
ax.plot(x,take,'-om')
ax.plot(x,ono,'-oc')
ax.plot(x,fuku,'-oy')
ax.legend([u'ทาเกฮาระ',u'โอโนมิจิ',u'ฟุกุยามะ'],loc=7,fancybox=1,shadow=1)
plt.show()