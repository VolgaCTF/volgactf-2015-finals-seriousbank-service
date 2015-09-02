from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from billings.models import AccountBilling
# Create your views here.

class UserHomePage(TemplateView):
	template_name = "cabinet/user_home.html"
	login_requred = "/login/"
	user = None

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			self.user = request.user
			context = self.get_context_data(**kwargs)
			return self.render_to_response(context)
		else:
			return HttpResponseRedirect(self.login_requred)

	def get_context_data(self, **kwargs):
		ctx = super(UserHomePage, self).get_context_data(**kwargs)
		if self.user is not None:
			query = AccountBilling.objects.filter(user_id=self.user.id)
			ctx['username'] = self.user.username
			ctx['account_summary'] = reduce(lambda acc, item: acc + item.bid, query, 0)
			ctx['billing_story'] = query.order_by("-transaction_timestamp")
		return ctx
