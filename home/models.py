from django.db import models

from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email


# Create your models here.
class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=70)
    email=models.CharField(max_length=70,default="")
    phone=models.CharField(max_length=70,default="")
    desc=models.CharField(max_length=300,default="")
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)
#this is for creation database objects through names of products
    def __str__(self) :
        return "Message from  " + self.name + "-" + self.email

class Profile(models.Model):
     user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
     email_token=models.CharField(max_length=200, blank=True, null=True)
     is_email_verified=models.BooleanField(default=False)

@receiver(post_save, sender=User)
def send_email_token(sender,instance,created, **kwargs):
    try:
        if created:
            email_token=str(uuid.uuid4())
            Profile.objects.create(user=instance,email_token=email_token)
            email=instance.email
            send_account_activation_email(email,email_token)
            
    except Exception as e:
        print(e)

    
