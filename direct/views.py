from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse,reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
@login_required
def inbox(request):
    user=request.user
    messages=Message.get_messages(user=user)
    active_direct=None
    directs=None
    if messages:
        message=messages[0]
        active_direct=message['user'].username
        directs=Message.objects.filter(user=user,recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread']=0
        context={
            'directs':directs,
            'messages':messages,
            'active_direct':active_direct,}

    template=loader.get_template('instagram/direct.html')
    return HttpResponse(template.render(context,request))

@login_required
def Directs(request,username):
    user=request.user
    messages=Message.get_messages(user=user)
    active_direct=username
    directs=Message.objects.filter(user=user,recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread']=0
    context={
        'directs':directs,
        'messages':messages,
        'active_direct':active_direct,


        }
    template=loader.get_template('instagram/direct.html')
    return HttpResponse(template.render(context,request))
@login_required
def SendDirect(request):
    from_user=request.user
    to_user_username=request.POST.get('to_user')
    body=request.POST.get('body')

    if request.method == 'POST':
        to_user=User.objects.get(username=to_user_username)
        Message.send_message(from_user,to_user,body)
        return redirect('inbox')
    else:
        HttpResponseBadRequest()

@login_required
def UserSearch(request):
    query=request.GET.get('q') #name=q in search_user.html
    context={}

    if query:
        users=User.objects.filter(Q(username__contains=query))

        #Pagination
        paginator=Paginator(users,6)
        page_number=request.GET.get('page')
        users_paginator=paginator.get_page(page_number)
        context={
            'users':users_paginator
            }
    template=loader.get_template('instagram/search_user.html')

    return HttpResponse(template.render(context,request))
@login_required
def NewConservation(request,username):
    from_user=request.user
    body="says hello"
    try:
        to_user=User.objects.get(username=username)
    except Exception as e:
        return redirect('usersearch')
    if from_user != to_user:
        Message.send_message(from_user,to_user,body)
    return redirect('inbox')

def checkDirects(request):
    directs_count=0
    if request.user.is_authenticated:
        directs_count=Message.objects.filter(user=request.user,is_read=False).count()
    return {'directs_count':directs_count}





            

