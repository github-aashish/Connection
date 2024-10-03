from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
# Create your views here.




def index(request):
    try:
        uid = request.session['logid']
    except:
        return redirect('login')
    try:
        Authenticated = User.objects.get(id=uid)
    except:
        Authenticated = None
    if Authenticated is not None:
        all_posts = Posts.objects.all().order_by('-date_created')
        suggestions = User.objects.all().exclude(username=Authenticated.username).order_by("?")[:6]
        context = {
            'user' : Authenticated,
            'posts' : all_posts,
            'suggestions' : suggestions
        }
        print(suggestions)
        return render(request,'index.html',context)
    else:
        return render(login)
    
    


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('uname')
        password = request.POST.get('password')
        try:
            Authenticated = User.objects.get(username=username,password=password)
        except:
            Authenticated = None
        if Authenticated is not None:
            request.session['logid']=Authenticated.id
            request.session['logname']=Authenticated.username
            request.session.save()
            #return HttpResponse("Authenticated Successfully")
            return redirect('index')
            #return render(request,'index.html',context)
        else:
            return redirect('login')
        
    

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('uname')
        useremail = request.POST.get('uemail')
        profileimage = request.FILES['profile']
        userpassword = request.POST.get('upassword')
        createUser = User(firstname=firstname,lastname=lastname,username=username,useremail=useremail,password=userpassword,pimage=profileimage)
        createUser.save()
        Follower.objects.create(user=createUser)
        return redirect('login')
        # print(firstname)
        # return HttpResponse("Done")
    else:
        return render(request, 'signup.html')
    
def logout(request):
        try:
            del request.session['logid']
            del request.session['logname']
        except:
            pass
        return redirect('login')
    
def createpost(request):
    if request.method == 'POST':
        uid = request.session['logid']
        try:
            user = User.objects.get(id=uid)
        except:
            user = None
        if user is not None:
            content = request.POST.get('content')
            medias = request.FILES.getlist('pimages')
            posts = Posts.objects.create(user=user,content=content)
            for media in medias:
                PostMedia.objects.create(post=posts,media=media)
            return redirect('index')
        else:
            return redirect('login')
        
def profile(request):
    try:
        uid = request.session['logid']
    except:
        return redirect('login')
    try:
        Authenticated = User.objects.get(id=uid)
    except:
        Authenticated = None
    if Authenticated is not None:
        all_posts = Posts.objects.filter(user=Authenticated).order_by('-date_created')
        suggestions = User.objects.all().exclude(username=Authenticated.username).order_by("?")[:6]
        context = {
            'user' : Authenticated,
            'posts' : all_posts,
            'suggestions' : suggestions
        }
        return render(request,'profile.html',context)
        
    else:
        return render(login)