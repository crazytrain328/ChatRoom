from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message,User
from django.db.models import Q 
from .forms import RoomForm, TopicForm, UserForm, MyUserCreationForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

# rooms = [
#     {'id':1 , 'name': 'Lets study Python'},
#     {'id':2 , 'name': 'Machine Learning'},
#     {'id':3 , 'name': 'Lets study Django'},
#     {'id':4 , 'name': 'My room'},
# ]

def loginPage(request):
    page='login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username= username)
        except :
            messages.error(request, 'User Not Found')
        
        user= authenticate(request, username= username,password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        
        else:
            messages.error(request,"Password or Username does not exist.")
 
 
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutPage(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'base/logout_register.html', {})

def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
    else:
        messages.error(request, 'An Error Has Occurred.')
    return render(request,'base/login_register.html', {'form':form})

    
    
     
    
def home(request):
    user = request.user if request.user.is_authenticated == True else ""
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q) |
        Q(name__icontains = q) |
        Q(description__icontains =q)
        )
    topics = Topic.objects.all()[0:6]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    room_count= rooms.count()
    context= {'rooms1': rooms,'topics': topics,'room_count': room_count,'user':user, 'room_messages':room_messages}
    return render(request, 'base/home.html',context)


def room(request,val):
    room = Room.objects.get(id= val)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message= Message.objects.create(
            user= request.user,
            room= room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', val= room.id)

    context= {'room3':room,'room_messages':room_messages,'participants':participants}
    return render(request, 'base/room.html',context)

@login_required(login_url= 'login')
def createRoom(request):
    form1 = RoomForm()
    topics= Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name= topic_name)
        Room.objects.create(
            host= request.user,
            topic= topic,
            name= request.POST.get('name'),
            description= request.POST.get('description')
        )
        
        return redirect('home')
            
    context={'form':form1,'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url= 'login')
def updateRoom(request, val):
    room = Room.objects.get(id= val)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse ('Since you are not the user,You are not allowed to update the room.')
    
    if request.method == 'POST':
        topic_name= request.POST.get('name')
        topic,created= Topic.objects.get_or_create(name= topic_name)
        room.topic= topic
        room.name=request.POST.get('name')
        room.host= request.user
        room.description= request.POST.get('description')
        room.save()
        return redirect('home')
    context= {'form':form}
    return render (request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, val):
    room = Room.objects.get(id=val)

    if request.user != room.host:
        return HttpResponse ('Since you are not the user,You are not allowed to delete the room.')

    if request.method =='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context= {'obj': room})


def deleteAll(request):
    rooms= Room.objects.all()
    if request.method == 'POST':
        for room in rooms:
            room.delete()
        return redirect('home')
    return render(request, 'base/delete_all.html', {})

def createTopic(request):
    form2= TopicForm()
    if request.method == 'POST':
        form= TopicForm(request.POST)
        if form.is_valid() == True:
            form.save()
            return redirect('home')
    context= {'form': form2}
    return render(request, 'base/topic_form.html', context)

@login_required(login_url='login')
def deleteMessage(request, val):
    message = Message.objects.get(id=val)
    if request.user != message.user:
        return HttpResponse ('Since you are not the user,You are not allowed here.')

    if request.method =='POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context= {'obj': message.body})

def userProfile(request,val):
    user= User.objects.get(id=val)
    rooms= user.room_set.all()
    room_messages = user.message_set.all()
    topics= Topic.objects.all()
    context={'user':user, 'rooms1': rooms, 'room_messages':room_messages, 'topics': topics}
    return render(request,'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user  
    form= UserForm(instance=user)
    if(request.method == 'POST'):
        form = UserForm(request.POST, request.FILES,instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', val=user.id )
    context= {'form':form}
    return render(request,'base/update-user.html',context)


def topicsPage(request):
    topics= Topic.objects.filter()
    return render(request, 'base/topics.html', {'topics':topics})