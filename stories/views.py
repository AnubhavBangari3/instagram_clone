from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from . models import *
from .forms import*

from django.http import JsonResponse
from datetime import  datetime,timedelta

# Create your views here.

@login_required
def NewStory(request):
    user=request.user
    file_objs=[]

    if request.method == 'POST':
        form=NewStoryForm(request.POST,request.FILES)
        if form.is_valid():
            file=request.FILES.get('content')
            caption=form.cleaned_data.get('caption')

            story=Story(user=user,content=file,caption=caption)
            story.save()
            return redirect('index')
    else:
        form=NewStoryForm()
    context={
        'form':form
        }
    return render(request,"instagram/newstory.html",context)
def ShowMedia(request, stream_id):
	stories = StoryStream.objects.get(id=stream_id)
	media_st = stories.story.all().values()

	stories_list = list(media_st)

	return JsonResponse(stories_list, safe=False)

    

