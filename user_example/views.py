from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user_example.models import Post
from django.contrib.auth.decorators import login_required
from .forms import UsersLoginForm
# from PIL import Image
from django.contrib.auth import authenticate, login
from .forms import UsersLoginForm
import os.path, time

@login_required
def index(request):
    posts = Post.objects.all()

    args = {'posts': posts}
    return render(request, 'user_example/index.html', args)

@csrf_exempt 
def getData(request):
    if request.method == 'POST':
        print('post', request.POST)
        print('file', request.FILES.get('upload_file'))
        name =  str(request.POST['name'])
        datetime = str(request.POST['time'])
        # print('time',time.strptime(datetime))
        image = request.FILES.get('upload_file')
        # print('****',name,time,image)
        ins = Post(Name = name, Time = datetime, Image = image)
        ins.save()


        print("saveData")
        # im = Image.open(request.FILES.get('upload_file'))
        # im.show()

        return HttpResponse("Your response")

def allData(request):
    posts = Post.objects.all()

    args = {'posts': posts}
    return render(request,'page/allData.html', args)

def groupData(request):
    return render(request,'page/groupData.html')

def searchData(request):
    return render(request,'page/searchData.html')

def settingCamera(request):
    return render(request,'page/settingCamera.html')

def actionDoor(request):
    return render(request,'page/actionDoor.html')

def notFound(request):
    return render(request,'page/notFound.html')