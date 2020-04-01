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


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    country = models.CharField(
        "Country",
        max_length=255,
    )

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
