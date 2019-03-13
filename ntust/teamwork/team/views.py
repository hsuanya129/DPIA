from django.shortcuts import render, get_object_or_404
from django.template import RequestContext 
from django.http import HttpResponseRedirect
from . import models
from .models import User
from .models import QuestionaryTemplate
# Create your views here.
def index(request):
    return render('team/home.html',locals())

def login(request):
    account = request.POST['account']
    password = request.POST['password']
    user = models.User.objects.filter(account=account,password=password)
    if len(user)==1:
        return render('team/choose_pia.html',locals())
    else:
        return render('team/home.html',locals())
def show_qn1(request):
	qn1_list = QuestionaryTemplate.objects.filter(questionary_type=1)
	path = request.path
	return render(request,'team/overview.html', locals())

