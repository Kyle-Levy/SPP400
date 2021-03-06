from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from datetime import timedelta
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.IntegerField(default=1)
    key_expiration = models.DateTimeField(default=timezone.now)

    def new_key(self):
        user = self.user
        self.key = random.randint(10000000, 99999999)
        self.save()
        email = EmailMessage('New authentication key', "Your new authentication key is: " + str(self.key), to=[user.email])
        email.send()

    def check_key(self, num):
        if self.user.email is None:
            return True
        if self.key == num:
            self.key_expiration = timezone.now() + timedelta(days=30)
            return True
        else:
            return False

    def expired(self):
        if timezone.now() > self.key_expiration:
            return True
        else:
            return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        instance.username = instance.username.lower()
        profile.save()
        instance.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.username == instance.username.lower():
        instance.username = instance.username.lower()
        instance.save()
    instance.profile.save()

