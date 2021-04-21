from django.urls import path
from .  views import *

urlpatterns=[
    
    path('newstory/',NewStory,name="newstory"),
   path('showmedia/<stream_id>', ShowMedia, name='showmedia'),
    ]