from django.db import models
from django.contrib.auth.models import User




class RequestBlood(models.Model):
	user = models.ForeignKey(to=User,on_delete=models.CASCADE,  blank=True, null=True)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.CharField(max_length=20)
	city = models.CharField(max_length=300, blank=True)
	blood_group = models.CharField(max_length=5)
	def __str__(self):
		return self.name

class Donor(models.Model):
	donor = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	phone = models.CharField(max_length=10)
	city = models.CharField(max_length=100)
	blood_group = models.CharField(max_length=5)
	def __str__(self):
		return self.blood_group

class AcceptedDonors(models.Model):
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=20)
	city = models.CharField(max_length=300, blank=True)
	blood_group = models.CharField(max_length=5)