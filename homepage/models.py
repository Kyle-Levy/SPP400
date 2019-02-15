from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import random
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.IntegerField(default=1)
    key_expiration = models.DateTimeField(default=datetime.now)

    def new_key(self):
        self.key = random.randint(1000, 9999)

    def check_key(self, num):
        if self.key == num:
            # self.new_key()
            return True
        else:
            return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

