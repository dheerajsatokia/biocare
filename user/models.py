from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models.functions import Concat


class User(AbstractUser):
    mobile_number = models.CharField(blank=True, max_length=50)

    # USER_TYPE_CHOICES = (
    #     ('PT', 'Patient'),
    #     ('DC', 'Doctor'),
    #     ('CH', 'Chemist'),
    #     ('LA', 'Lab Operator'),
    #     ('SA', 'Super Admin'),
    # )
    #
    # type = models.CharField(max_length=2,
    #                         choices=USER_TYPE_CHOICES,
    #                         null=False, blank=False, default="PT")

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)


class ForgetPasswordToken(models.Model):
    token = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exp_time = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.exp_time


# class Doctor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='Doctor')
#     speciality = models.CharField(max_length=50, null=False)
#     department = models.CharField(max_length=50, null=False)
#     prescription_chem = models.TextField()
#     prescription_lab = models.TextField()
#     remarks = models.TextField()
#
#
# class Patient(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='patient')
#     age = models.IntegerField(null=False)
#     blood_group = models.CharField(max_length=5)
#
#
# class LabOperator(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='lab_operator')
# #
#
# class Chemist(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='chemist', default=3)
