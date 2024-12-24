from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Profile, Department, Stream, Post, Tag, Follow, Likes, Message, FriendRequest
from .forms import NewPostform,EditProfileForm
from django.urls import resolve, reverse
from django.http import HttpResponseRedirect
from django.db import transaction
# Create your views here.

def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username , password = password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is incorrect')
                return redirect('login')

        return render(request,"login.html")

def log_out(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        class CreateUser(UserCreationForm):
            email = forms.EmailField(required=True)
            department = forms.CharField(max_length=100, help_text='department')
            skills = forms.CharField(max_length=500, help_text='skills')
            class Meta:
                model = User
                fields = ['username','email','password1','password2','department','skills']

        form = CreateUser()

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password1')
            department = request.POST.get('department')
            skills = request.POST.get('skills')

            form = CreateUser(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                Profile.objects.create(
                    user = user,
                    department = department,
                    skills = skills,
                    first_name = username
                )

                messages.success(request, 'Account was created for '+username)
                return redirect('login')

        departments = Department.objects.all() 
        context = {"form" : form, 'departments':departments}
        return render(request,'register.html',context)

@login_required(login_url='login')
def home(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    liked_posts = Likes.objects.filter(user=user)
    suggestions = Profile.objects.filter(department=user.profile.department)
    received_requests = FriendRequest.objects.filter(recipient=request.user,accepted=False,declined=False)

    group_ids = []
    liked_posts_ids = []
    for post in posts:
        group_ids.append(post.post_id)
        
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    for liked_post in liked_posts:
        liked_posts_ids.append(liked_post.post)

    skills = request.user.profile.skills
    skillsSet = skills.split(',')
    skillsSet = [element for element in skillsSet if element]

    if request.method == 'POST':
            query = request.POST.get('search')
            if query:
                results = Profile.objects.filter(first_name__icontains=query) | Profile.objects.filter(skills__icontains=query)
            else:
                 results = None

            context = {'results': results}

            print(results)

            # return redirect('my_collab',context)
            return render(request,'my_collab.html',context)

    context = {'post_items':post_items, 'skills' : skillsSet, 'liked_posts_ids': liked_posts_ids, 'suggestions':suggestions, 'received_requests':received_requests}
    return render(request,'home.html',context)

@login_required(login_url='login')
def my_collab(request):
    user = request.user

    profiles = Profile.objects.all()
    followings = Follow.objects.filter(follower=user)

    following_ids = [following.following for following in followings]

    context = {'profiles': profiles, 'following_ids': following_ids}
    return render(request,'my_collab.html',context)

@login_required(login_url='login')
def messaging(request):
    user = request.user

    messages = Message.get_message(user=request.user)
    active_direct = None
    directs = None
    profile = get_object_or_404(Profile, user=user)

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=request.user, reciepient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs':directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile,
    }

    return render(request,'msg/messaging.html',context)

@login_required(login_url='login')
def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        if to_user_username is None:
            return redirect('messaging')
        else:
            to_user = User.objects.get(username=to_user_username)
            
        Message.sender_message(from_user, to_user, body)
        
        return redirect('messaging')

@login_required
def Directs(request, username):
    user  = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username)  
    directs.update(is_read=True)

    for message in messages:
            if message['user'].username == username:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'msg/messaging.html', context)

def NewPost(request):
    user = request.user
    tags_obj = []
    
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            print(tag_form)
            tag_list = tag_form.split(",")

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tag.set(tags_obj)
            p.save()
            return redirect('home')
    else:
        form = NewPostform()
    context = {
        'form': form
    }
    return render(request, 'newpost.html', context)


def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()
    
    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    skillSets = profile.skills.split(',')
    skillSet = skillSets[:-1]

    user = request.user
    tags_obj = []
    
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            print(tag_form)
            tag_list = tag_form.split(",")

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tag.set(tags_obj)
            p.save()
            return redirect('home')
    else:
        form = NewPostform()

    sent_requests = FriendRequest.objects.filter(sender=request.user, recipient=get_object_or_404(User, username=username))
    accepted_requests = {req for req in sent_requests if req.accepted}
    declined_requests = {req for req in sent_requests if req.declined}

    print(accepted_requests)
    print(declined_requests)

    context = {
        'posts': posts,
        'profile':profile,
        'posts_count':posts_count,
        'skills':skillSet,
        'following_count':following_count,
        'followers_count':followers_count,
        'follow_status':follow_status,
        'form':form,
        'accepted_requests' : accepted_requests,
        'declined_requests' : declined_requests,
        'sent_requests' : sent_requests,
    }


    return render(request, 'profile.html', context)


# Like function
@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    # return HttpResponseRedirect(reverse('post-details', args=[post_id]))
    return HttpResponseRedirect(reverse('home'))

def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))

def profile_edit(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == "POST":
        print("Entered Post")
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            profile.profile_pic = form.cleaned_data.get('profile_pic')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.bio = form.cleaned_data.get('bio')
            profile.skills = form.cleaned_data.get('skills')
            print(profile.first_name)
            print(profile.first_name)
            profile.save()
            return redirect('profile', profile.user.username)
    else:
        form = EditProfileForm()

    context = {
        'form' : form
    }

    return render(request,'profile_edit.html',context)

@login_required
def send_friend_request(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    FriendRequest.objects.create(sender=request.user, recipient=recipient)
    messages.success(request, f"Friend request sent to {recipient.username}.")
    return HttpResponseRedirect(reverse('profile', kwargs={'username': recipient.username}))


@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    friend_request.accepted = True
    friend_request.save()
    content = "Hey there you are accepted by "+friend_request.sender.username
    messages.success(request, f"You are now friends with {friend_request.sender.username}.")
    from_user = request.user
    to_user = User.objects.get(username=friend_request.sender.username)
    body = content
    Message.sender_message(from_user, to_user, body)
    return redirect('messaging')

@login_required
def decline_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    friend_request.declined = True
    friend_request.save()
    messages.warning(request, f"You declined the friend request from {friend_request.sender.username}.")
    return redirect('home')