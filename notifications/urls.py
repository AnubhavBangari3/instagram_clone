from django.urls import path
from .  views import *

urlpatterns=[
    path('',ShowNotifications,name="show-notifications"),
    path('<noti_id>/delete',DeleteNotification,name="delete-notifications")
    ]