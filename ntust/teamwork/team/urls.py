from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login_sign/$', views.login_sign, name='login_sign'),
	url(r'^questionary/(?P<questionary_type_id>[-\d]+)$', views.questionary, name='questionary'),
	url(r'^new_pia/',views.new, name='new_pia'),
	url(r'^login_sign/sign',views.sign, name='sign'),
	url(r'^home/',views.home, name='home'),
	url(r'^stakeholder/',views.stakeholder, name='stakeholder'),
	url(r'^dataflow/',views.dataflow, name='dataflow'),
	url(r'^dataflow_get/',views.dataflow_get, name='dataflow_get'),
	url(r'^dataflow_saveTemp/',views.dataflow_saveTemp, name='dataflow_saveTemp'),
	url(r'^dataflow_saveLane/',views.dataflow_saveLane, name='dataflow_saveLane'),
	url(r'^evaluation/',views.evaluation, name='evaluation'),
	url(r'^risk_mapping/',views.risk_mapping, name='risk_mapping'),
	url(r'^pia_examine/',views.pia_examine, name='pia_examine'),
	url(r'^choose_pia/',views.choose_pia, name='choose_pia'),
]