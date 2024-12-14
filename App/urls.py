from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('index',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('userNameCheck/<str:userName>',views.userNameCheck,name='userNameCheck'),
    path('logout',views.logout,name='logout'),
    path('createpost',views.createpost,name='createpost'),
    path("n/post/<int:id>/like", views.like_post, name="likepost"),
    path("n/post/<int:id>/unlike", views.unlike_post, name="unlikepost"),
    path("n/post/<int:id>/save", views.save_post, name="savepost"),
    path("n/post/<int:id>/unsave", views.unsave_post, name="unsavepost"),
    path("n/post/<int:post_id>/comments", views.comment, name="comments"),
    path("n/post/<int:post_id>/write_comment",views.comment, name="writecomment"),
    path("<str:username>/follow", views.follow, name="followuser"),
    path("<str:username>/unfollow", views.unfollow, name="unfollowuser"),
    path('profile/<str:username>',views.profile,name='profile'),
    path('notification',views.notification,name='notification'),
    path('search',views.search,name='search'),
    path('edit-profile',views.editProfile,name='editProfile'),
    path('delete-post',views.deletePost,name='deletePost'),
    path('connections',views.connections,name='connections'),
    path('changeImage', views.changeImage,name='changeImage'),
    path('saved',views.saved,name='saved'),
    path('messaging',views.messaging,name='messaging'),
    path('chat-history/<int:user_id>/', views.chat_history, name='chat_history'),
]