from django.shortcuts import render,render_to_response, get_object_or_404
from django.template import RequestContext 
from django.http import HttpResponseRedirect
from . import models
from .models import User
# Create your views here.
def index(request):
    return render_to_response('team/home.html',locals())

def login(request):
    account = request.POST['account']
    password = request.POST['password']
    user = models.User.objects.filter(account=account,password=password)
    if len(user)==1:
        return render_to_response('team/choose_pia.html',locals())
    else:
        return render_to_response('team/home.html',locals())