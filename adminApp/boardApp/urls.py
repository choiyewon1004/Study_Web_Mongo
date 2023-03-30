from django.urls import path
from boardApp import views
urlpatterns=[
    path('index/', views.main , name = 'index'),
    path('login/', views.login),
    path('list/', views.list, name ='list'),
    path('joinForm/', views.joinForm),
    path('join/', views.join),
    path('bbsForm/', views.registerForm),
    path('register/', views.register),
    path('view/', views.read),
    path('delete/', views.delete),
    path('update/', views.update),
    path('logout/', views.logout),
    path('search/', views.search),

]