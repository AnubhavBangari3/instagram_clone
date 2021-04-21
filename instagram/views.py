from django.shortcuts import render,redirect,get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse,reverse_lazy

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . models import *

from django.contrib.auth.forms import *
from .forms import*

from post.models import *
from django.core.paginator import Paginator
from django.urls import resolve
from django.template import loader

from django.views import generic
from django.views.generic import *

from django.db import transaction
#A transaction is an atomic set of database queries. Even if your program crashes, 
#the database guarantees that either all the changes will be applied, 
#or none of them.

# Create your views here.
def UserProfile(request,username):
    user=get_object_or_404(User,username=username)
    profile=Profile.objects.get(user=user)
    url_name=resolve(request.path).url_name
    if url_name=='profile':
        posts=Post.objects.filter(user=user).order_by('-posted')
    else:
        posts=profile.favourites.all()
    #Profile information stats
    posts_count=Post.objects.filter(user=user).count()
    following_count=Follow.objects.filter(follower=user).count()
    followers_count=Follow.objects.filter(following=user).count()
    #check follow status
    follow_status=Follow.objects.filter(following=user,follower=request.user).exists()

    paginator=Paginator(posts,6)
    page_number=request.GET.get('page')
    posts_paginator=paginator.get_page(page_number)
    template=loader.get_template('instagram/profile.html')

    context={
        'posts':posts_paginator,
        'profile':profile,
        'url_name':url_name,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'follow_status':follow_status,
        }
    return HttpResponse(template.render(context,request))
@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	BASE_WIDTH = 400

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('index')
	else:
		form = EditProfileForm()

	context = {
		'form':form,
	}

	return render(request, 'instagram/profile_edit.html', context)


@login_required
def follow(request,username,option):
    user=request.user
    following=get_object_or_404(User,username=username)
    try:
        f,created=Follow.objects.get_or_create(follower=user,following=following)
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following,user=user).all().delete()
        else:
            posts=Post.objects.all().filter(User=following)[:10]
            with transaction.atomic():
                for post in posts:
                    stream=Stream(post=post,user=user,date=post.posted,following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile',args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile',args=[username]))

##no need for login_required here
def login_view(request):
    if request.method=='POST':
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(User,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(reverse('index'))
        else:
            return render(request,"instagram/login.html")
    else:
        return render(request,"instagram/login.html")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
def register(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('login'))
        else:
            pass
            
    else:
        form=SignUpForm()
        return render(request,"instagram/register.html",{"form":form})
            
     

            









        


    
