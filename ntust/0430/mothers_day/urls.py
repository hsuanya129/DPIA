from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.index,name='index'),#主畫面
	url(r'^write/$', views.write, name='write'), 
]