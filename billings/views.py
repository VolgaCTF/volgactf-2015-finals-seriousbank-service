from django.shortcuts import render
from django.views.generic.edit import View
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from billings.forms import BillingForm
from billings.helpers import set_cookie, gen_password, validate_permissions
from billings.crypto import DESCryptor

# Create your views here.

class CreateBilling(View):
	form_class = BillingForm
	default_cryptor = DESCryptor
	success_url = "/home/"
	template_name = "billings/billing.html"

	def get(self, request):
		form = self.form_class(initial={ 'bid': '0', 'sign': '' })
		return render(request, self.template_name, {'form' : form, })

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			if request.user.is_authenticated():
				billing = form.save(commit=False)
				billing.user = request.user
					
				_cryptor = self.default_cryptor(*gen_password(request.user.password))
				billing.sign = _cryptor.encrypt(billing.sign.encode('ascii'))

				billing.transaction_timestamp = timezone.now()
				billing.save()
				response = HttpResponseRedirect(self.success_url)
				set_cookie(response, 'accepted_transaction', billing.sign)
				return response
			else:
				form.add_error(None, "User must be logged in to create billings")		
		return render(request, self.template_name, {'form' : form })


class ValidateTransaction(View):
	default_cryptor = DESCryptor

	def get(self, request, name):
		user = User.objects.get(username__iexact=name)
		transaction = request.COOKIES.get('accepted_transaction')
		if transaction is not None:
			billing = user.accountbilling_set.get(sign__iexact=transaction)
			passwd = gen_password(user.password)
			_cryptor = self.default_cryptor(*passwd)
			sign = _cryptor.decrypt(billing.sign)
			if validate_permissions(request.user, name):
				return HttpResponse(sign)
			else:
				return HttpResponse('502')
		else:
			return HttpResponse('404')