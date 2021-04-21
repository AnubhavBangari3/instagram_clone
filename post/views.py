from django.shortcuts import render,redirect,get_object_or_404
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.urls import reverse
from instagram.models import Profile
from stories.models import *
from comment.models import *
from comment.forms import *
# Create your views here.

@login_required
def index(request):
    user=request.user
    posts=Stream.objects.filter(user=user)
    stories=StoryStream.objects.filter(user=user)


    group_ids=[]
    for post in posts:
        group_ids.append(post.post_id)

    post_items=Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    template=loader.get_template('instagram/index.html')

    context={
        "post_items":post_items,
        "stories":stories
        }

    return HttpResponse(template.render(context,request))
@login_required
def PostDetails(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    user=request.user
    favourited=False
    #comments
    comments=Comment.objects.filter(post=post).order_by('date')
    #comment form
    if request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.user=user
            comment.save()
            return HttpResponseRedirect(reverse('postdetails',args=[post_id]))
    else:
        form=CommentForm()


    #favourite color conditions
    if request.user.is_authenticated:
        profile=Profile.objects.get(user=request.user)
        #for the color of favourite button
        if profile.favourites.filter(id=post_id).exists():
            favourited=True

    template=loader.get_template('instagram/post_detail.html')
    context={
        "post":post,
        "favourited":favourited,
        "form":form,
        "comments":comments
        }
    return HttpResponse(template.render(context,request))


@login_required
def NewPost(request):
    user=request.user
    tag_objs=[]
    file_objs=[]

    if request.method =='POST':
        form=NewPostForm(request.POST,request.FILES)
        if form.is_valid():
            files=request.FILES.getlist('content')
            caption=form.cleaned_data.get('caption')
            tags_form=form.cleaned_data.get('tags')

            tags_list=list(tags_form.split(','))

            for tags in tags_list:
                t,created=Tag.objects.get_or_create(title=tags)
                tag_objs.append(t)

            for file in files:
                file_instance=PostFileContent(file=file,user=user)
                file_instance.save()
                file_objs.append(file_instance)

            p,created=Post.objects.get_or_create(caption=caption,user=user)
            p.tags.set(tag_objs)
            p.content.set(file_objs)
            p.save()
            return redirect('index')
    else:
        form=NewPostForm()
    context={
            'form':form
            }


    return render(request,'instagram/newpost.html',context)
@login_required
def tags(request,tag_slug):
    tag=get_object_or_404(Tag,slug=tag_slug)
    posts=Post.objects.filter(tags=tag).order_by("-posted")
    template=loader.get_template('instagram/tag.html')
    context={"posts":posts,
             "tag":tag
             }
    return HttpResponse(template.render(context,request))



@login_required
def like(request,post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    current_likes=post.likes
    liked=Like.objects.filter(user=user,post=post).count()

    if not liked:
        like=Like.objects.create(user=user,post=post)
        current_likes=current_likes+1
    else:
        Like.objects.filter(user=user,post=post).delete()
        current_likes=current_likes-1 
    post.likes=current_likes
    post.save()
    return HttpResponseRedirect(reverse('postdetails',args=[post_id]))

@login_required
def favourite(request,post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    profile=Profile.objects.get(user=user)
    if profile.favourites.filter(id=post_id).exists():
        profile.favourites.remove(post)
    else:
        profile.favourites.add(post)
    return HttpResponseRedirect(reverse('postdetails',args=[post_id]))





        





