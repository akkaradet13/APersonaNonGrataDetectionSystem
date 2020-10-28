from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user_example.models import Post
from PIL import Image

def index(request):
    posts = Post.objects.all()

    args = {'posts': posts}
    return render(request, 'user_example/index.html', args)

@csrf_exempt 
def getData(request):
    print('12346')
    if request.method == 'POST':
        print('post', request.POST)
        print('file', request.FILES.get('upload_file'))
        postName =  str(request.POST['postName'])
        description = str(request.POST['description'])
        time = str(request.POST['time'])
        image = request.FILES.get('upload_file')
        ins = Post(postName = postName, description = description, time = time, image = image)
        ins.save()
        print("saveData")
        # im = Image.open(request.FILES.get('upload_file'))
        # im.show()

        return HttpResponse("Your response")