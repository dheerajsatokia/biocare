from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    mobile_number = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.email


class ForgetPasswordToken(models.Model):
    token = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exp_time = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.exp_time
