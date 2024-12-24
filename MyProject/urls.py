"""
URL configuration for MyProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MyApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.log_in, name = 'login'),
    path('register',views.register,name = 'register'),
    path('home',views.home, name = 'home'),
    path('my_collab',views.my_collab, name = 'my_collab'),

    #Message Section
    path('msg/messaging',views.messaging, name = 'messaging'),
    path('msg/<username>', views.Directs, name="directs"),
    path('send/', views.SendDirect, name="send-directs"),


    path('logout',views.log_out,name = 'logout'),
    path('newpost',views.NewPost, name = 'newpost'),
    path('<uuid:post_id>/like', views.like, name='like'),

    # profile
    path('<username>/', views.UserProfile, name='profile'),
    path('<username>/follow/<option>/', views.follow, name='follow'),
    path('profile/edit', views.profile_edit, name="editprofile"),

    #friend request
    path('send-request/<int:recipient_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline-request/<int:request_id>/',views.decline_friend_request, name='decline_friend_request'),
]

urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)