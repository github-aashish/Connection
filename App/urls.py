from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
    path('index',views.index,name='index'),
    path('createpost',views.createpost,name='createpost'),
    path('profile',views.profile,name='profile'),
]