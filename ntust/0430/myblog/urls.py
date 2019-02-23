from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.blog, name='blog'),
    url(r'^add/', views.add, name="add"),
    url(r'^edit/', views.edit, name="edit"),
]