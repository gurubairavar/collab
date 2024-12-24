from django.contrib import admin
from MyApp.models import Post, Tag, Follow, Stream, Profile, Likes, Message,FriendRequest,Department

# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Profile)
admin.site.register(Likes)
admin.site.register(Message)
admin.site.register(FriendRequest)
admin.site.register(Department)