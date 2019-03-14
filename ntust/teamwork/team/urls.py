from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login, name='login'),
	url(r'^overview/$', views.show_qn1, name='show_qn1'),
	url(r'^new_pia/',views.new, name='new_pia'),
	url(r'^sign/',views.sign, name='sign'),
	url(r'^home/',views.home, name='home'),
]