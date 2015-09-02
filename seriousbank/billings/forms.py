from django import forms
from billings.models import AccountBilling

class BillingForm(forms.ModelForm):
	bid = forms.IntegerField(label="Bid value", min_value=1, max_value=100500, widget=forms.NumberInput)
	sign = forms.CharField(label="CVC", max_length=150, widget=forms.TextInput)
	class Meta:
		model = AccountBilling
		fields = ('bid', 'sign',)
