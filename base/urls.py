from django.urls import path,include
from . import views

urlpatterns=[
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutPage, name='logout'),
    path('register/',views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('room/<str:val>/', views.room, name= 'room'),
    path('profile/<str:val>/', views.userProfile, name= 'user-profile'),
    path('create_room/', views.createRoom, name='create-room'),
    path('update_room/<str:val>/', views.updateRoom, name='update-room'),
    path('delete_room/<str:val>/', views.deleteRoom, name='delete-room'),
    path('delete_all_rooms', views.deleteAll, name='delete-all-rooms'),
    path('create_new_topic', views.createTopic, name='create-new-topic'),
    path('delete-message/<str:val>/', views.deleteMessage, name='delete-message'),
    path('update-user/', views.updateUser, name= 'update-user'),
    path('topics-page/', views.topicsPage, name= 'topics-page')
]