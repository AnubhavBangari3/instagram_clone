from django.contrib import admin
from post.models import*
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
