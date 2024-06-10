from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib import messages


# Create your models here.
class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    author=models.CharField(max_length=25)
    title=models.CharField(max_length=225)
    views=models.IntegerField(default=0)
    content=HTMLField()
    slug=models.CharField(max_length=300)
    datetime=models.DateField( blank=True)
    # thumbnail = models.ImageField(upload_to='blog/images', default="")
    
#this is for creation database objects through names of products
    def __str__(self) :
        return  self.title + " by "  +  self.author
  
class BlogComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)

    def __str__(self) :
            return  self.comment[0:13] + "..." + "by" + " " +  self.user.username
    

