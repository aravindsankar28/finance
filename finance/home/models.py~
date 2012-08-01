from django.db import models
from django.contrib.auth.models import User
class events(models.Model):
	name = models.CharField(max_length = 50)
	venue = models.CharField(max_length = 100)
	description=models.TextField(max_length=1000)
	event_id=models.AutoField(primary_key=True)
	date = models.DateField()
    
class UserEvent(models.Model):
	user = models.ForeignKey(User)
	event = models.ForeignKey(events)
# Create your models here.
	
class Budget(models.Model):
	event = models.ForeignKey(events)
	#user = models.ForeignKey(User)
	budgetid = models.AutoField(primary_key = True)
	planA = models.CharField(max_length = 10)
	planB = models.CharField(max_length = 10)
	approve = models.BooleanField(default = False)
	item_approval = models.BooleanField(default = False)
class SplitA(models.Model):
	budgetid = models.DecimalField(decimal_places = 0 ,max_digits = 10)
	item = models.CharField(max_length = 25)
	price = models.DecimalField(decimal_places = 2,max_digits = 10)
	balance = models.DecimalField(decimal_places = 2,max_digits = 10)
	status = models.CharField(max_length = 10)
	approve = models.BooleanField(default = False)
	spid = models.AutoField(primary_key = True)
	amount_debit = models.DecimalField(decimal_places = 2,max_digits = 10)
class SplitB(models.Model):
	budgetid = models.DecimalField(decimal_places = 0 ,max_digits = 10)
	item = models.CharField(max_length = 25)
	price = models.DecimalField(decimal_places = 2,max_digits = 10)
	balance = models.DecimalField(decimal_places = 2,max_digits = 10)
	status = models.CharField(max_length = 10)