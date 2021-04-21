from django.urls import path
from .  views import *

urlpatterns=[
    path('',inbox,name="inbox"), 
    path('directs/<username>',Directs,name="directs"),
    path('send/',SendDirect,name="send_direct"),
    path('new/',UserSearch,name="usersearch"),
    path('new/<username>',NewConservation,name="newconservation")
    ]