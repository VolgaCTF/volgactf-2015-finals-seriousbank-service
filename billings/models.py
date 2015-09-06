from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AccountBilling(models.Model):
	user = models.ForeignKey(User)
	bid = models.IntegerField(default=None)
	sign = models.CharField(max_length=150)
	transaction_timestamp = models.DateTimeField()

class ValidatedTransaction(models.Model):
	username = models.CharField(max_length=30)
	tranzaction_id = models.CharField(max_length=500)
	is_validated = models.BooleanField()