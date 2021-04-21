from django.contrib.auth.models import User
from django.db import models
from datetime import *

from django.db.models.signals import post_save,post_delete
from django.utils.text import slugify
from django.urls import reverse
import uuid
from notifications.models import Notification
##post models
def user_directory_path(instance,filename):
    #will upload to MEDIA_ROOt/user(id)/filename
    return 'user-{0}/{1}'.format(instance.user.id,filename)

class Tag(models.Model):
    title=models.CharField(max_length=120,verbose_name="Tag")
    slug=models.SlugField(null=False,unique=True) #A slug field in Django is used to store and 
                                                          #generate valid URLs for your dynamically 
                                                          #created web page

    class Meta:
        verbose_name_plural="Tags"
    def get_absolute_url(self):
        return reverse('tags',args=[self.slug])
    def __str__(self):
        return self.title
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        return super().save(*args,**kwargs)

class PostFileContent(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='content_owner')
    file=models.FileField(upload_to=user_directory_path)


class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    content=models.ManyToManyField(PostFileContent,related_name='contents')
    caption=models.TextField(max_length=120,verbose_name="Caption")
    posted=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tag,related_name="tags")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)
    def get_absolute_url(self):
        return reverse('postdetails',args=[str(self.id)])
    #def __str__(self):
        #return self.posted

class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")

    def user_follow(sender,instance,*args,**kwrags):
        follow=instance
        sender=follow.follower
        following=follow.following
        notify=Notification(sender=sender,user=following,notification_type=3)
        notify.save()

    def user_unfollow(sender,instance,*args,**kwargs):
        follow=instance
        sender=follow.follower
        following=follow.following

        notify=Notification.objects.filter(sender=sender,user=following,notication_type=3)
        notify.delete()

class Stream(models.Model):
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="stream_following")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    def add_post(sender,instance,*args,**kwargs):
        post=instance
        user=post.user
        followers=Follow.objects.all().filter(following=user)

        for follower in followers:
            stream=Stream(post=post,user=follower.follower,date=post.posted,following=user)
            stream.save()

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_like")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_likes")
    def user_liked_post(sender,instance,*args,**kwargs):
        like=instance
        post=like.post
        sender=like.user
        notify=Notification(post=post,sender=sender,user=post.user,notification_type=1)

        notify.save()

    def user_unlike_post(sender,instance,*args,**kwargs):
        like=instance
        post=like.post
        sender=like.user

        notify=Notification.objects.filter(post=post,sender=sender,notification_type=1)
        notify.delete()

    #stream
post_save.connect(Stream.add_post,sender=Post)
#likes
post_save.connect(Like.user_liked_post,sender=Like)
post_delete.connect(Like.user_unlike_post,sender=Like)

#follow
post_save.connect(Follow.user_follow,sender=Follow)
post_delete.connect(Follow.user_unfollow,sender=Follow)
















