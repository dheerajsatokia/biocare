from django.db import models
from user.models import User


# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kyc_doc1 = models.FileField(upload_to='DoctorKYC/', null=True, blank=True)
    kyc_doc2 = models.FileField(upload_to='DoctorKYC/', null=True, blank=True)
    is_kyc_approved = models.BooleanField(default=False)


class Chemist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kyc_chem1 = models.FileField(upload_to='ChemistKYC/', null=True, blank=True)
    kyc_chem2 = models.FileField(upload_to='ChemistKYC/', null=True, blank=True)
    is_kyc_approved = models.BooleanField(default=False)


class LabUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kyc_lab1 = models.FileField(upload_to='LabUSerKYC/', null=True, blank=True)
    kyc_lab2 = models.FileField(upload_to='LabUSerKYC/', null=True, blank=True)
    is_kyc_approved = models.BooleanField(default=False)
