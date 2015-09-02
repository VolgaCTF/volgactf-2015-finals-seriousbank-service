from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AccountBilling(models.Model):
	user = models.ForeignKey(User)
	bid = models.IntegerField(default=None)
	sign = models.CharField(max_length=150)
	transaction_timestamp = models.DateTimeField()