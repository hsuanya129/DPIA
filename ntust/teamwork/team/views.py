from django.shortcuts import render, get_object_or_404
from django.template import RequestContext 
from django.http import HttpResponseRedirect, HttpResponse
from . import models
from .models import User,Question,QuestionaryType,Answer,Stakeholder
import pdb
from django.urls import reverse
import datetime

base_url = "http://127.0.0.1:8000/"

def index(request):
    return render(request,'team/home.html/',locals())

def login_sign(request):

    if request.method == "POST":
        if 'login' in request.POST:#一個表單兩個action時要用到 此為按下登入時觸發的action
            account = request.POST['account']
            password = request.POST['password']
            user = models.User.objects.filter(account=account,password=password)
            if len(user) != 0:
                return render(request,'team/choose_pia.html/',locals())
            else:
                # return render(request,'team/home.html',locals())
                return HttpResponseRedirect('/team/') 
        else:#此為按下註冊時觸發的action
            return render(request,'team/sign.html',locals())
    return render(request, 'team/home.html',locals())

def questionary(request, questionary_type_id=None):

    if questionary_type_id is not None and int(questionary_type_id) in (1, 2, 3):

        qn_type = QuestionaryType.objects.get(id=questionary_type_id)

        qn_list = Question.objects.filter(questionary_type_id=questionary_type_id)
    else:
        return HttpResponse('wrong url.')

    if request.method == "POST": #如果表單送出(POST)

        
        answer_list = list() #初始化LIST變數
        #queryset是django的obects的型別，跟list一樣，Object[0]，這個就是Model的Object，
        #locals()代表該funtion所夾帶的所有變數，
        
        for i in range(len(qn_list)): 
            answer_list.append(request.POST.get('answer'+ str(i+1))) 
            # 取得 input name="answer1~10" 的 value 並加入到 answer_list
        
        for i in range(len(qn_list)):
            
            if answer_list[i] != '':
                Answer.objects.create(
                    question_id=qn_list[i].id,
                    context=answer_list[i],
                    activity_id=1 #test id 
                )

        if questionary_type_id == '1' or '2':

            return HttpResponseRedirect(base_url + 'team/questionary/' + str(int(questionary_type_id)+1))

        elif questionary_type_id == '3':

            return render(request,'team/stakeholder.html', locals())

        

        '''
        pdb.set_trace()
        如果要在這裡停，以上的變數都會被記錄，執行到這行，CMD裡就會停
        停下後就可以在CMD裡面做運算(ctrl+z可以取消該次請求，輸入c(等於continue的意思)會繼續執行)
        '''
        
    return render(request,'team/questionary.html', locals()) #第三個變數代表會傳給第二個變數規定的html的變數有哪些

def stakeholder(request):
    if 'ok' in request.POST:
        name = request.POST['name']
        role = request.POST['role']
        email = request.POST['email']
        part = request.POST['part']
        feedback = request.POST['feedback']
        Stakeholder.objects.create(name=name, role=role, email=email, part=part, feedback=feedback)

    return render(request, 'team/stakeholder.html', locals())
def new(request):
    if request.method == 'POST':
        name = request.POST.get('pia_name','')
        piam_name = request.POST.get('piam_name','')
        piam_email = request.POST.get('piam_email','')
        activity_manager_name = request.POST.get('activitym_name','')
        activity_manager_email = request.POST.get('activitym_email','')
        today = datetime.date.today()
        description = request.POST.get('description','')
        user = models.Activity.objects.create(name=name,pia_manager_name=piam_name,pia_manager_email=piam_email,activity_manager_name=activity_manager_name,activity_manager_email=activity_manager_email,date=today,description=description)
        return render(request,'team/choose_pia.html', locals())
    return render(request,'team/new_pia.html', locals())
    
def home(request):
    return render(request,'team/home.html', locals())

def sign(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        account = request.POST.get('account','')
        password = request.POST.get('password','')
        user = models.User.objects.create(name=name,account=account, password=password,permission_level=1,activity_id=1)
        return HttpResponseRedirect('/team/')
    return HttpResponseRedirect('/team/')

