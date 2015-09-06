"""seriousbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from accounts.views import RegisterFormView, LoginFormView, LogOutView, account
from billings.views import CreateBilling, ValidateTransaction
from cabinet.views import UserHomePage
from seriousbank.views import IndexPage


urlpatterns = [
    url(r'^register/$', RegisterFormView.as_view()),
    url(r'^login/$', LoginFormView.as_view()),
    url(r'^logout/$', LogOutView.as_view()),
    url(r'^billing/$', CreateBilling.as_view()),
    url(r'^billing/(?P<name>[\w]{0,50})/$', ValidateTransaction.as_view()),
    url(r'^home/$', UserHomePage.as_view()),
    url(r'^$', IndexPage.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
