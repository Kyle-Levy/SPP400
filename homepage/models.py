from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length = 1000)
    password = models.CharField(max_length = 1000) #edit this later to make it encryptable
    email = models.CharField(max_length=1000)
    phone = models.IntegerField()
    title = models.CharField(max_length = 100)
    uuid = models.IntegerField()


#class set_password(self, raw_password):
