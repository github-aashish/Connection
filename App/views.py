from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import *
import json
from django.core.paginator import Paginator
import numpy as np
from PIL import Image
from io import BytesIO
# Create your views here.
from deepface import DeepFace
#django 3.0.7 version


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
        notification = Notification.objects.get(user=Authenticated)
        all_posts = Posts.objects.all().order_by('-date_created')
        #all_posts = Posts.objects.all().order_by('?')
        # pagination = Paginator(all_posts,5)
        # pageno = request.GET.get('page')
        # final_posts = pagination.get_page(pageno)
        followings = Follower.objects.filter(followers=Authenticated).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=Authenticated.username).order_by("?")[:6]
        context = {
            'user' : Authenticated,
            'notification' : notification,
            'posts' : all_posts,
            'suggestions' : suggestions
        }
        #print(suggestions)
        return render(request,'index.html',context)
    else:
        return redirect(login)
    
    


def login(request):
    if request.method == "GET":
        try:
            uid = request.session['logid']
        except:
            uid = None
        if uid is None:
            return render(request, 'login.html')
        else:
            return redirect('index')
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
            messages.error(request, "Invalid username or password")
            return redirect('login')
        
    

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('uname')
        useremail = request.POST.get('uemail')
        profileimage = request.FILES['profile']
        userpassword = request.POST.get('upassword')
        try:
            isexist = User.objects.get(Q(username = username) | Q(useremail = useremail))
        except:
            isexist = None
        if isexist is None:
            createUser = User(firstname=firstname,lastname=lastname,username=username,useremail=useremail,password=userpassword,pimage=profileimage,backupimage=profileimage)
            createUser.save()
            Follower.objects.create(user=createUser)
            Notification.objects.create(user=createUser)
            return redirect('login')
        else:
            messages.error(request, "User with same email or username already exists")
            return redirect('signup')
        # print(firstname)
        # return HttpResponse("Done")
    else:
        return render(request, 'signup.html')
    
def userNameCheck(request,userName):
    if request.method == 'GET':
        userExist = User.objects.filter(username=userName)
        if len(userExist) > 0:
            return JsonResponse({},status=200)
        else:
            return JsonResponse({},status=404)
            
    
def logout(request):
        try:
            del request.session['logid']
            del request.session['logname']
            messages = None
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
        
        
@csrf_exempt
def like_post(request, id):
    if request.method == 'PUT':
            try:
                uid = request.session['logid']
            except:
                return redirect('login')
            try:
                Authenticated = User.objects.get(id=uid)
            except:
                Authenticated = None
            if Authenticated is not None:
                post = Posts.objects.get(pk=id)
                if post.user == Authenticated:
                    pass
                else:
                    usernotification = Notification.objects.get(user=post.user)
                    usernotification.status = True
                    usernotification.save()
                    NotificationMsgs.objects.create(user=post.user,from_user=Authenticated,for_post=post,msg="Liked Your Post")
                try:
                    post.likers.add(Authenticated)
                    post.save()
                    return HttpResponse(status=204)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return redirect('login') 
    else:
        return HttpResponse("Method must be 'PUT'")
    
    

@csrf_exempt
def unlike_post(request, id):
        if request.method == 'PUT':
            try:
                uid = request.session['logid']
            except:
                return redirect('login')
            try:
                Authenticated = User.objects.get(id=uid)
            except:
                Authenticated = None
            if Authenticated is not None:
                post = Posts.objects.get(pk=id)
                print(post)
                try:
                    post.likers.remove(Authenticated)
                    post.save()
                    return HttpResponse(status=204)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return redirect('login') 
        else:
            return HttpResponse("Method must be 'PUT'")

@csrf_exempt
def save_post(request, id):
        if request.method == 'PUT':
            try:
                uid = request.session['logid']
            except:
                return redirect('login')
            try:
                Authenticated = User.objects.get(id=uid)
            except:
                Authenticated = None
            if Authenticated is not None:
                post = Posts.objects.get(pk=id)
                try:
                    post.savers.add(Authenticated)
                    post.save()
                    return HttpResponse(status=204)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return redirect('login')
        else:
            return HttpResponse("Method must be 'PUT'")

@csrf_exempt
def unsave_post(request, id):
    if request.method == 'PUT':
            try:
                uid = request.session['logid']
            except:
                return redirect('login')
            try:
                Authenticated = User.objects.get(id=uid)
            except:
                Authenticated = None
            if Authenticated is not None:
                post = Posts.objects.get(pk=id)
                try:
                    post.savers.remove(Authenticated)
                    post.save()
                    return HttpResponse(status=204)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return redirect('login')
    else:
        return HttpResponse("Method must be 'PUT'")


@csrf_exempt
def comment(request, post_id):
        if request.method == 'POST':
            data = json.loads(request.body)
            comment = data.get('comment_text')
            post = Posts.objects.get(id=post_id)
            try:
                uid = request.session['logid']
            except:
                return redirect('login')
            try:
                Authenticated = User.objects.get(id=uid)
            except:
                Authenticated = None
            if Authenticated is not None:
                try:
                    newcomment = Comment.objects.create(post=post,commenter=Authenticated,comment_content=comment)
                    post.comment_count += 1
                    post.save()
                    if post.user == Authenticated:
                        pass
                    else:
                        usernotification = Notification.objects.get(user=post.user)
                        usernotification.status = True
                        usernotification.save()
                        NotificationMsgs.objects.create(user=post.user,from_user=Authenticated,for_post=post,msg="Commented on your Post")
                    #print(newcomment.serialize())
                    return JsonResponse([newcomment.serialize()], safe=False, status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return redirect('login')
    
        post = Posts.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        comments = comments.order_by('-comment_time').all()
        return JsonResponse([comment.serialize() for comment in comments], safe=False)
    
    
@csrf_exempt
def follow(request, username):
        if request.method == 'PUT':
            try:
                uid = request.session['logid']
            except:
                return redirect('login')
            try:
                Authenticated = User.objects.get(id=uid)
            except:
                Authenticated = None
            if Authenticated is not None:
                try:
                    user = User.objects.get(username=username)
                except:
                    user = None
                print(f".....................User: {user}......................")
                print(f".....................Follower: {request.user}......................")
                try:
                    (follower, create) = Follower.objects.get_or_create(user=user)
                    (chatUser, create) = ChatList.objects.get_or_create(user=user)
                    (chatUser2, create) = ChatList.objects.get_or_create(user=Authenticated)
                    
                    follower.followers.add(Authenticated)
                    follower.save()
                    chatUser.chatUsers.add(Authenticated)
                    chatUser.save()
                    chatUser2.chatUsers.add(user)
                    chatUser2.save()
                    usernotification = Notification.objects.get(user=user)
                    usernotification.status = True
                    usernotification.save()
                    NotificationMsgs.objects.create(user=user,from_user=Authenticated,msg="Sends Connection")
                    return HttpResponse(status=204)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return redirect('login')
        else:
            return HttpResponse("Method must be 'PUT'")

@csrf_exempt
def unfollow(request, username):
        if request.method == 'PUT':
            try:
                uid = request.session['logid']
            except:
                return redirect('login')
            try:
                Authenticated = User.objects.get(id=uid)
            except:
                Authenticated = None
            if Authenticated is not None:
                try:
                    user = User.objects.get(username=username)
                except:
                    user = None
                print(f".....................User: {user}......................")
                print(f".....................Unfollower: {Authenticated.username}......................")
                try:
                    follower = Follower.objects.get(user=user)
                    follower.followers.remove(Authenticated)
                    follower.save()
                    return HttpResponse(status=204)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return redirect('login')
        else:
            return HttpResponse("Method must be 'PUT'")



def profile(request,username):
    
    try:
        uid = request.session['logid']
    except:
        return redirect('login')
    try:
        user = User.objects.get(username=username)
        Authenticated = User.objects.get(id=uid)
    except:
        Authenticated = None
    if Authenticated is not None:
        isFollower = False
        all_posts = Posts.objects.filter(user=user).order_by('-date_created')
        followings = Follower.objects.filter(followers=Authenticated).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=Authenticated.username).order_by("?")[:6]
        following_count = Follower.objects.filter(followers=user).count()
        try:
            follower_count = Follower.objects.get(user=user).followers.all().count()
            if Authenticated in Follower.objects.get(user=user).followers.all():
                isFollower = True
        except:
            follower_count = 0
            isFollower = False
        context = {
            'user' : Authenticated,
            "username": user,
            'posts' : all_posts,
            'suggestions' : suggestions,
            'follower_count' : follower_count,
            'following_count' : following_count,
            'is_follower' : isFollower,
            
        }
        return render(request,'profile.html',context)
        
    else:
        return redirect(login)
    
def notification(request):
    try:
        uid = request.session['logid']
    except:
        return redirect('login')
    try:
        Authenticated = User.objects.get(id=uid)
    except:
        Authenticated = None
    if Authenticated is not None:
        usernotification = Notification.objects.get(user=Authenticated)
        usernotification.status = False
        usernotification.save()
        notificationsmessages = NotificationMsgs.objects.filter(user=Authenticated)
        notification = Notification.objects.get(user=Authenticated)
        followings = Follower.objects.filter(followers=Authenticated).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=Authenticated.username).order_by("?")[:6]
        context = {
            'user' : Authenticated,
            'notification' : notification,
            'suggestions' : suggestions,
            'notimsgs' : notificationsmessages
        }
    #return HttpResponse("Notifications")
    return render(request, 'notification.html', context)


def saved(request):
    try:
        uid = request.session['logid']
    except:
        return redirect('login')
    try:
        Authenticated = User.objects.get(id=uid)
    except:
        Authenticated = None
    if Authenticated is not None:
        all_posts = Posts.objects.filter(savers=Authenticated).order_by('-date_created')
        notification = Notification.objects.get(user=Authenticated)
        followings = Follower.objects.filter(followers=Authenticated).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=Authenticated.username).order_by("?")[:6]
        context = {
            'user' : Authenticated,
            'notification' : notification,
            'posts' : all_posts,
            'suggestions' : suggestions
        }
        return render(request, 'saved.html', context)
    else:
        return redirect('login')
    
def search(request):
    global searcheduser
    try:
        uid = request.session['logid']
    except:
        return redirect('login')
    try:
        Authenticated = User.objects.get(id=uid)
    except:
        Authenticated = None
    if Authenticated is not None:
        notification = Notification.objects.get(user=Authenticated)
        #all_posts = Posts.objects.all().order_by('-date_created')
        usersuggestions = User.objects.all().exclude(username=Authenticated.username).order_by("?")[:6]
        followings = Follower.objects.filter(followers=Authenticated).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=Authenticated.username).order_by("?")[:6]
        if request.method=='POST':
            username = request.POST.get('username')
            found = False
            if username == '':
                userimage = request.FILES['searchimage']
                searchImage = Image.open(userimage)
                image_array = np.array(searchImage)
                found_id = None
                try :
                    dfs = DeepFace.find(img_path=image_array,db_path="media/searches/")
                    userstring = str(dfs[0]['identity'].iloc[0])
                    originalString = userstring[6:]
                    searcheduser = User.objects.values('id', 'backupimage')
                    for item in searcheduser:
                        if item['backupimage'] == originalString:
                            found_id = item['id']
                            break
                    searcheduser = User.objects.filter(id=found_id).first()
                    found = True
                except:
                    messages.error(request, "User Not Found with This Face")
                    searcheduser = False
            else:
                try:
                    searcheduser = User.objects.get(username = username)
                    found = True
                except:
                    found = False
                    
                print("*****************************************")
                print(found)
            if found == False:
                global message
                messages.error = (request,"User Not Found with This Face or User Name")
                
        else:
            searcheduser = False
        context = {
            'user' : Authenticated,
            'notification' : notification,
            'suggestions' : suggestions,
            'searcheduser':searcheduser,
            'usersuggestions':usersuggestions,
        }
        #print(suggestions)
        return render(request,'search.html',context)
    else:
        return redirect(login)
   
@csrf_exempt    
def editProfile(request):
    if request.method == 'PUT':
            data = json.loads(request.body)
            uId = data.get('user_id')
            userName = data.get('user_name')
            userBio = data.get('user_bio')
            try:
                editUser = User.objects.get(id=int(uId))
            except:
                editUser = None
            if editUser is not None:
                editUser.username = userName
                editUser.bio = userBio
                editUser.save()
                return JsonResponse({}, status=200)
            else:
                return JsonResponse({}, status=400)
            
@csrf_exempt
def changeImage(request):
    if request.method == 'POST':
            try:
                uid = request.session['logid']
            except:
                return redirect('login')
            try:
                Authenticated = User.objects.get(id=uid)
            except:
                Authenticated = None
            if Authenticated is not None:
                profileimage = request.FILES['profile']
                Authenticated.pimage = profileimage
                Authenticated.save()
                return redirect('profile', Authenticated.username)
                
            else:
                return redirect('login')
        
    
     
@csrf_exempt
def deletePost(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        postId = data.get('post_id')
        try:
            userPost = Posts.objects.get(id=int(postId))
        except:
            userPost = None
        if userPost is not None:
            userPost.delete()
            return JsonResponse({}, status=200)
        else:
             return JsonResponse({}, status=400)
    else:
        return HttpResponse("Method Should be Delete")
             
    
def connections(request):
    try:
        uid = request.session['logid']
    except:
        return redirect('login')
    try:
        Authenticated = User.objects.get(id=uid)
    except:
        Authenticated = None
    if Authenticated is not None:
        notification = Notification.objects.get(user=Authenticated)
        followings = Follower.objects.filter(followers=Authenticated).values_list('user', flat=True)
        authenticated_followings = Follower.objects.filter(followers=Authenticated).order_by('user')
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=Authenticated.username).order_by("?")[:6]
        context = {
            'user' : Authenticated,
            'notification' : notification,
            'suggestions' : suggestions,
            'authenticated_followings':authenticated_followings,
        }
        #print(suggestions)
        return render(request,'connections.html',context)
    else:
        return redirect('login')
    
def messaging(request):
    if request.method == 'GET':
        try:
            uid = request.session['logid']
        except:
            return redirect('login')
        try:
            Authenticated = User.objects.get(id=uid)
        except:
            Authenticated = None
        if Authenticated is not None:
            notification = Notification.objects.get(user=Authenticated)
            chatlist = ChatList.objects.filter(user=Authenticated).values_list('chatUsers', flat=True)
            #authenticated_followings = Follower.objects.filter(followers=Authenticated).order_by('user')
            suggestions = User.objects.filter(pk__in=chatlist).exclude(username=Authenticated.username)
            print(suggestions)
            context = {
                'user' : Authenticated,
                'notification' : notification,
                'suggestions' : suggestions,
                #'authenticated_followings':authenticated_followings,
            }
        return render(request,'chat.html',context)
    
def chat_history(request, user_id):
    try:
            uid = request.session['logid']
    except:
            return redirect('login')
    try:
            Authenticated = User.objects.get(id=uid)
    except:
            Authenticated = None
    if Authenticated is not None:
        receiver = get_object_or_404(User, id=user_id)
        # Fetch all messages between the logged-in user and the receiver
        messages = ChatMessage.objects.filter(
            sender=Authenticated, receiver=receiver
        ) | ChatMessage.objects.filter(
            sender=receiver, receiver=Authenticated
        ).order_by('timestamp')
        print(messages)
        messages_list = [
            {
                "sender": msg.sender.username,
                "receiver": msg.receiver.username,
                "message": msg.message,
                #"timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp": msg.timestamp.strftime("%H:%M"),
                
            }
            for msg in messages
        ]
        return JsonResponse({"messages": messages_list,'receiverImage':receiver.pimage.url,'receiverFirstName':receiver.firstname,'receiverLastName':receiver.lastname})

    return JsonResponse({"error": "Not authenticated"}, status=401)