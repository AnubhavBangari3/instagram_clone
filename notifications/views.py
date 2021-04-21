from django.shortcuts import render,redirect,get_object_or_404
from django.db import IntegrityError

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from notifications.models import *
from .models import *
from django.template import loader

# Create your views here.
#notifications

def ShowNotifications(request):
    user=request.user
    notifications=Notification.objects.filter(user=user).order_by('-date')
    Notification.objects.filter(user=user,is_seen=False).update(is_seen=True)

    template=loader.get_template('instagram/notifications.html')
    context={
        'notifications':notifications
             }

    return HttpResponse(template.render(context,request))

def DeleteNotification(request,noti_id):
    user=request.user
    Notification.objects.filter(id=noti_id,user=user).delete()
    return redirect('show-notifications')

def CountNotifications(request):
    count_notifications=0
    if request.user.is_authenticated:
        count_notifications=Notification.objects.filter(user=request.user,is_seen=False).count()
    return {
        'count_notifications':count_notifications
            }