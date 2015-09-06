from django.shortcuts import render
from django.views.generic.edit import View
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, Http404
from django.contrib.auth.models import User
from billings.forms import BillingForm
from billings.helpers import set_cookie, gen_password, validate_permissions
from billings.crypto import DESCryptor
from billings.validate import TransactionValidator

# Create your views here.

class CreateBilling(View):
	form_class = BillingForm
	default_cryptor = DESCryptor
	default_validator = TransactionValidator
	success_url = "/user/%d/"
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

				try:
					billing.sign = _cryptor.encrypt(billing.sign.encode('ascii'))
				except Exception as ex:
					return HttpResponseServerError(str(ex).encode('utf-8'))

				billing.transaction_timestamp = timezone.now()
				billing.save()

				_validator = self.default_validator()

				try:
					trz_data = _validator.invalidate(request.user.username, billing.sign)
				except Exception as ex:
					return HttpResponseServerError(str(ex).encode('utf-8'))

				response = HttpResponseRedirect(self.success_url % request.user.id)
				set_cookie(response, 'accepted_transaction', trz_data)
				return response
			else:
				form.add_error(None, "User must be logged in to create billings")		
		return render(request, self.template_name, {'form' : form })


class ValidateTransaction(View):
	default_cryptor = DESCryptor
	default_validator = TransactionValidator

	def get(self, request, name):
		user = User.objects.get(username__iexact=name)
		transaction = request.COOKIES.get('accepted_transaction')
		if transaction is not None:

			_validator = self.default_validator()

			try:
				transaction_id = _validator.get_id(transaction)
			except Exception as ex:
				raise Http404(ex)

			passwd = gen_password(user.password)
			_cryptor = self.default_cryptor(*passwd)

			try:
				sign = _cryptor.decrypt(transaction_id)
			except Exception as ex:
				return HttpResponseServerError(str(ex).encode('utf-8'))
				

			if validate_permissions(request.user, name):
				if _validator.validate(name, transaction_id):
					return HttpResponse(sign)
				else:
					raise Http404("User don't have this transaction")
			else:
				raise Http404("User don't have permissions to validate transaction")
		else:
			raise Http404("Transaction is empty")