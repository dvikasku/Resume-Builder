from django.contrib import admin
from django.urls import path , include
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('resume/', views.resume, name='resume'),
    path('logged', views.logged, name='logged'),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('activate/<uidb64>/<token>',views.get,name = 'activate'),
]
