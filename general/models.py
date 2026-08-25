from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    class Type(models.TextChoices):
        moderator = 'moderator', 'модератор'
        builder = 'builder', 'сборщик'
        reader = 'reader', 'читатель'
        
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    type = models.TextField(choices=Type, null=True)
    # totp_key = models.TextField(max_length=128, null=True)
    
    # class Meta:
    #     parmissions = [
    #         (),
    #         (),
    #     ]
        
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)