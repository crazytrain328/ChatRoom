from django.db import models 
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass
    name= models.CharField(max_length=200, null=True)
    email= models.EmailField(unique= True,null= True)
    bio = models.TextField(null = True)

    avatar= models.ImageField(null= True, default="avatar.svg") 

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

class Topic(models.Model):
    name= models.TextField()

    def __str__(self):
        return self.name

class Room(models.Model):
    topic= models.ForeignKey(Topic, on_delete=models.SET_NULL, null= True)
    host= models.ForeignKey(User,on_delete= models.SET_NULL, null= True)
    name= models.CharField(max_length=200)
    description= models.TextField(null=True, blank= True)
    participants= models.ManyToManyField(User,related_name='participants',blank=True)
    # auto_now takes timestamp everytime we save it
    # auto_now_add takes timestamp only once.

    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now= True)

     


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', '-updated']

class Message(models.Model):

    user= models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) ## One to Many Relationship (One room can have multiple messages but one text can only
    # belong to a single room.)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.body[0:50]
    
    class Meta:
        ordering = ['-created', '-updated']

