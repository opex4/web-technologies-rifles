from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import pyotp

# Create your models here.
class UserProfile(models.Model):
    class Type(models.TextChoices):
        moderator = 'moderator', 'модератор'
        builder = 'builder', 'сборщик'
        reader = 'reader', 'читатель'
        
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    type = models.TextField(choices=Type, null=False, verbose_name="Тип пользователя", default=Type.reader)
    totp_key = models.CharField(max_length=128, null=False, blank=False)
    
    class Meta:
        verbose_name = "Расширение пользователя"
        verbose_name_plural = "Расширения пользователей"

    def save(self, *args, **kwargs):
        if self.id is None:
            self.totp_key = pyotp.random_base32()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.type
        
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        