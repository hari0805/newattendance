from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from crm1 import settings
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=200, null=True)
	designation = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_of_join = models.DateTimeField(auto_now_add=True, null=True)
	date_of_birth = models.DateTimeField(auto_now_add=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Attendance(models.Model):
	attender = models.CharField(max_length=25,null=True)
	date = models.DateField(null=True)
	is_present = models.BooleanField(null=True)
	clockin = models.DateTimeField(null=True)
	clockout = models.DateTimeField(null=True)

	def __str__(self):
		return str(self.attender) + " " + str(self.clockin)[:19]

class leave_choice(models.Model):
	choice = models.CharField(max_length=25)

	def __str__(self):
		return self.choice

# str(self.attender.username) + " " + str(self.clockin)[:19]