
from django.contrib.auth.models import User
from django.db import models
from datetime import *
from post.models import Post
from django.db.models.signals import post_save
from PIL import Image
from django.conf import settings
import os

def user_directory_path(instance,filename):
    #will upload to MEDIA_ROOt/user(id)/filename
    profile_pic_name='user-{0}/{1}'.format(instance.user.id,filename)
    full_path=os.path.join(settings.MEDIA_ROOT,profile_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    else:
        pass
    return profile_pic_name
     
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=120,null=True,blank=True)
    last_name=models.CharField(max_length=120,null=True,blank=True)
    location=models.CharField(max_length=120,null=True,blank=True)
    url=models.CharField(max_length=120,null=True,blank=True)
    created=models.DateField(auto_now_add=True)
    favourites=models.ManyToManyField(Post)
    picture=models.ImageField(upload_to='user_directory_path',null=True,blank=True,verbose_name="profile_picture")

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        SIZE=300,300

        if self.picture:
            pic=Image.open(self.picture.path)
            pic.thumbnail(SIZE,Image.LANCZOS)
            pic.save(self.picture.path)
        
        
        
    def create_user_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)
        else:
            pass
    def save_user_profile(sender,instance,**kwargs):
        instance.profile.save()



    post_save.connect(create_user_profile,sender=User)
    post_save.connect(save_user_profile,sender=User)

# post_save - but sent at the end of the save() method.


     



