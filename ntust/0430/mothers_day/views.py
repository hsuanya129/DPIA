from django.shortcuts import render,render_to_response,get_object_or_404
from django.template import loader
from django.http import Http404,HttpResponseRedirect
from django.http import HttpResponse
from . import models
import datetime
from .models import Cards

def index(request):
	latest_cards_list = Cards.objects.all()
	return render_to_response('mothers_day/index.html',locals())

def write(request):
	
	title =request.POST['title']
	user_name = request.POST['user_name']
	content = request.POST['content']
	pub_date = datetime.datetime.now()
	cards = models.Cards(title=title,user_name=user_name,content=content,pub_date=pub_date)
	cards.save()
	return HttpResponseRedirect('/mothers_day/')
	

