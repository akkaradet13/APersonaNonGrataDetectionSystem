from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user_example.models import Post
from django.contrib.auth.decorators import login_required
from .forms import UsersLoginForm
# from PIL import Image
from django.contrib.auth import authenticate, login
from .forms import UsersLoginForm
import datetime, random, requests
from pymongo import MongoClient

@login_required
def index(request):
    return render(request, 'user_example/index.html')

@csrf_exempt 
def getData(request):
    # try:
    #     connect = MongoClient()
    #     print("connect successfully!!!")
    # except:
    #     print("could not connect to MongoDB")

    if request.method == 'POST':
        print('post', request.POST)
        print('file', request.FILES.get('upload_file'))
        Name =  str(request.POST['name'])
        dateTime = str(request.POST['dateTime'])
        Image = request.FILES.get('upload_file')
        ins = Post(Name = Name, DateTime = datetime.datetime.fromisoformat(dateTime), Image = Image)
        ins.save()
        print("saveData")
        # im = Image.open(request.FILES.get('upload_file'))
        # im.show()

        # db = connect.APersonaNonGrataData
        # db.user_example_post.insert_one(
        #     {
        #         "Name": Name,
        #         "DateTime": datetime.datetime.fromisoformat(dateTime),
        #         "Image": Image
        #     })

        return HttpResponse("Your response")

def allData(request):
    posts = Post.objects.all()
    args = {'posts': posts}
    try:
        formDate = request.GET['fromDate']
        toDate = request.GET['toDate']
        print(formDate,toDate)
        args = {
            'posts': posts,
            'fromDate' : formDate,
            'toDate' : toDate
        }
        return render(request,'page/allData.html', args)
    except:
        args = {
            'posts': posts
        }
        print('null')
        return render(request,'page/allData.html', args)
    # return render(request,'page/allData.html', args)

def groupData(request):
    return render(request,'page/groupData.html')

def searchData(request):
    '''
    from pymongo import MongoClient

    try:
        connect = MongoClient()
        print("connect successfully!!!")
    except:
        print("could not connect to MongoDB")

    db = connect.APersonaNonGrataData
    db.user_example_post.insert_one(
        {
            "Name": "test01",
            "id": 2,
            "Id": 2,
            "DateTime": datetime.datetime.fromisoformat('2011-11-05 00:05:23.283'),
            "Image": "image/1012202020-12-10_152001.110588..jpg"
        })
        '''
    # try:
    #     formDate = request.GET['fromDate']
    #     toDate = request.GET['toDate']
    #     print(formDate,toDate)
    #     data = {
    #         'fromDate' : formDate,
    #         'toDate' : toDate
    #     }
    #     return render(request,'page/searchData.html', data)
    # except:
    #     print('null')
    # Name = 'test_01'
    # DateTime = datetime(2015, 10, 9, 23, 55, 59, 342380)
    # Image = 'image/1012202020-12-10_151953.648711..jpg'
    # ins = Post(Name = Name, DateTime = DateTime, Image = Image)
    # ins.save()
    # print('***')
    return render(request,'page/searchData.html')

def settingCamera(request):
    try :
        valueSecurity = request.GET['valueSecurity']
        print('valueSecurity', valueSecurity)
        data = {'valueSecurity': valueSecurity}
    except :
        data = {'valueSecurity': '1'}
        print('---')
    return render(request,'page/settingCamera.html', data)

def actionDoor(request):
    try :
        value = request.GET['value']
        print('value', value)
        if value == 'Open':
            print('open')
            x = requests.get('http://192.168.43.9/actionDoor/0')
            print('open',x.status_code)
        else:
            print('closed')
            x = requests.get('http://192.168.43.9/actionDoor/1')
            print('close',x.status_code)
    except:
        values = random.randint(0,1)
    return render(request,'page/actionDoor.html')

def notFound(request):
    return render(request,'page/notFound.html')