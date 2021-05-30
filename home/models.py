from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    dob = models.CharField(max_length=55)
    address = models.CharField(max_length=455)  
    email = models.EmailField()
    linkedin = models.URLField(blank=True)
    phone = models.CharField(max_length=10)
    about = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images" , default="")


    def full_name(self):
        return " ".join([self.first_name, self.last_name])

class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_st = models.DateTimeField(auto_now = True)
    otp = models.SmallIntegerField()