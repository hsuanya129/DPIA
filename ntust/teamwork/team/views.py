from django.shortcuts import render, get_object_or_404
from django.template import RequestContext 
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from . import models
from .models import *
import pdb
from django.urls import reverse
import datetime
import json

base_url = "http://127.0.0.1:8000/"

def index(request):
    return render(request,'team/home.html/',locals())

def login_sign(request):

    if request.method == "POST":
        if 'login' in request.POST:#一個表單兩個action時要用到 此為按下登入時觸發的action
            account = request.POST['account']
            password = request.POST['password']
            user = User.objects.filter(account=account,password=password)
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
        user = Activity.objects.create(name=name,pia_manager_name=piam_name,pia_manager_email=piam_email,activity_manager_name=activity_manager_name,activity_manager_email=activity_manager_email,date=today,description=description)
        return HttpResponseRedirect('/team/questionary/1')
        # return render(request,'team/questionary/1', locals())
    return render(request,'team/new_pia.html', locals())
    
def home(request):
    return render(request,'team/home.html', locals())

def sign(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        account = request.POST.get('account','')
        password = request.POST.get('password','')
        user = User.objects.create(name=name,account=account, password=password,permission_level=1,activity_id=1)
        return HttpResponseRedirect('/team/')
    return HttpResponseRedirect('/team/')

def dataflow(request):
    pk =2
    swimlane_objects = Swimlane.objects.filter(activity_id=pk)
    if len(swimlane_objects) == 0:
        Swimlane.objects.create(activity_id= pk)

    if request.method == 'POST':
        swimlane_object_post = Swimlane.objects.get(activity_id=pk)
        data_text = request.POST.get('postdata')
        data_json = json.loads(data_text)
        swimlane_object_post.swimlane_json = data_json  
        swimlane_object_post.save()

    return render(request, 'team/dataflow.html')

def dataflow_get(request):
    pk=2
    swimlane_object_get = Swimlane.objects.get(activity_id=pk)
    if json.dumps(swimlane_object_get.swimlane_json) == "{}":
        swimlane_object_one = Swimlane.objects.get(activity_id=1)
        swimlane_object_get.swimlane_json = swimlane_object_one.swimlane_json
        Process.objects.create(activity_id=pk,name="Collect")
        Process.objects.create(activity_id=pk,name="Store")
        Process.objects.create(activity_id=pk,name="Use")
        Process.objects.create(activity_id=pk,name="Transfer")
        Process.objects.create(activity_id=pk,name="Delete")
    return JsonResponse(swimlane_object_get.swimlane_json)

def dataflow_saveTemp(request):
    pk=2
    saveTemp = request.POST.get('postdata')
    saveTemp = json.loads(saveTemp)

    if saveTemp["event"]=="addNode":
        addNode(saveTemp,pk)
    elif saveTemp["event"]=="removeNode":
        removeNode(saveTemp,pk)
    elif saveTemp["event"]=="rename" :
        renameNode(saveTemp,pk)

    return render(request, 'team/dataflow.html')

def addNode(saveTemp,pk):

    
    if saveTemp["asset_type"] =="Lane1":
        if len(Participant.objects.filter(activity_id=pk, name=saveTemp["name"])) == 0:
            Participant.objects.create(activity_id=pk, name=saveTemp["name"])
        participant = Participant.objects.get(activity_id=pk, name=saveTemp["name"])
        process = Process.objects.get(activity_id=pk, name=saveTemp["process"])
        if len(ProcessHasParticipant.objects.filter(process_id=process.id,participant_id=participant.id)) == 0:
            ProcessHasParticipant.objects.create(process_id=process.id,participant_id=participant.id)

    elif saveTemp["asset_type"] == "Lane2":
        if len(System.objects.filter(activity_id=pk, name=saveTemp["name"])) ==0:
            System.objects.create(activity_id=pk, name=saveTemp["name"])
        system = System.objects.get(activity_id=pk, name=saveTemp["name"])
        process = Process.objects.get(activity_id=pk, name=saveTemp["process"])
        if len(ProcessHasSystem.objects.filter(process_id =process.id,system_id=system.id)) ==0:
            ProcessHasSystem.objects.create(process_id =process.id,system_id=system.id)

    elif (saveTemp["asset_type"]=="Lane3" or saveTemp["asset_type"]=="Lane5") :
        if len(Pii.objects.filter(activity_id=pk, name=saveTemp["name"])) ==0:
            Pii.objects.create(activity_id=pk, name=saveTemp["name"])
        pii = Pii.objects.get(activity_id=pk, name=saveTemp["name"])
        process = Process.objects.get(activity_id=pk, name=saveTemp["process"])
        if len(ProcessHasPii.objects.filter(process_id =process.id,pii_id=pii.id)) ==0:
            ProcessHasPii.objects.create(process_id =process.id,pii_id=pii.id)

def removeNode(saveTemp,pk):
    if saveTemp["asset_type"] =="Lane1":
        participant = Participant.objects.get(activity_id=pk, name=saveTemp["name"])
        process = Process.objects.get(activity_id=pk, name=saveTemp["process"])
        itemDelete = ProcessHasParticipant.objects.get(process_id =process.id,participant_id=participant.id)
        itemDelete.delete()

    elif saveTemp["asset_type"] == "Lane2":
        system = System.objects.get(activity_id=pk, name=saveTemp["name"])
        process = Process.objects.get(activity_id=pk, name=saveTemp["process"])
        itemDelete =ProcessHasSystem.objects.get(process_id =process.id,system_id=system.id)
        itemDelete.delete()

    elif (saveTemp["asset_type"]=="Lane3" or saveTemp["asset_type"]=="Lane5") :
        pii = Pii.objects.get(activity_id=pk, name=saveTemp["name"])
        process = Process.objects.get(activity_id=pk, name=saveTemp["process"])
        itemDelete =ProcessHasPii.objects.get(process_id =process.id,pii_id=pii.id)
        itemDelete.delete()

def renameNode(saveTemp,pk):
    swimlane = Swimlane.objects.get(activity_id=pk)
    nodeDataArray = swimlane.swimlane_json['nodeDataArray']
    process = Process.objects.get(activity_id=pk, name=saveTemp['process'])

    if saveTemp["asset_type"] =="Lane1":
        participant_old = Participant.objects.get(activity_id=pk, name=saveTemp['old_name'])
        if len(ProcessHasParticipant.objects.filter(participant_id=participant_old.id))==1: #舊的name只有一個物件
            if len(Participant.objects.filter(activity_id=pk, name=saveTemp['name'])) ==0: #新的name尚未有物件
                participant_old.name = saveTemp['name']
                participant_old.save()
                print("it's first circumstance")

            elif len(Participant.objects.filter(activity_id=pk, name=saveTemp['name'])) ==1: #新的name已有物件
                participant_new = Participant.objects.get(activity_id=pk, name=saveTemp['name'])
                participant_old.delete()
                ProcessHasParticipant.objects.create(participant_id=participant_new.id,process_id=process.id)
                print("it's second circumstance")

        elif len(ProcessHasParticipant.objects.filter(participant_id=participant_old.id))!=1: #舊的name不只有一個物件
            if len(Participant.objects.filter(activity_id=pk, name=saveTemp['name'])) ==0: #新的name尚未有物件
                Participant.objects.create(activity_id=pk, name=saveTemp['name'])
                participant_new = Participant.objects.get(activity_id=pk, name=saveTemp['name'])
                processHasParticipant_old = ProcessHasParticipant.objects.get(process_id=process.id,participant_id=participant_old.id)
                processHasParticipant_old.delete()
                ProcessHasParticipant.objects.create(process_id=process.id,participant_id=participant_new.id)
                print("it's third circumstance")

            elif len(Participant.objects.filter(activity_id=pk, name=saveTemp['name'])) ==1: #新的name已有物件
                participant_new = Participant.objects.get(activity_id=pk, name=saveTemp['name'])
                processHasParticipant_old = ProcessHasParticipant.objects.get(process_id=process.id,participant_id=participant_old.id)
                processHasParticipant_old.delete()
                ProcessHasParticipant.objects.create(process_id=process.id,participant_id=participant_new.id)
                print("it's forth circumstance")

    elif saveTemp["asset_type"] == "Lane2":
        if len(System.objects.filter(activity_id = pk ,name = saveTemp['name'])) ==0:
            system = System.objects.get(activity_id=pk, name=saveTemp["old_name"])
            system.name = saveTemp["name"]
            system.save()

            for node in nodeDataArray:
                if node.get("group") != None:
                    if node['group'] == "Lane2" and node['text'] == saveTemp["old_name"]:
                        node['text'] = saveTemp["name"]

    elif (saveTemp["asset_type"]=="Lane3" or saveTemp["asset_type"]=="Lane5") :
        if len(Pii.objects.filter(activity_id = pk ,name = saveTemp['name'])) ==0:
            pii = Pii.objects.get(activity_id=pk, name=saveTemp["old_name"])
            pii.name = saveTemp["name"]
            pii.save()

            for node in nodeDataArray:
                if node.get("group") != None:
                    if (node['group'] == "Lane3" or "Lane5") and node['text'] == saveTemp["old_name"]:
                        node['text'] = saveTemp["name"]

    elif saveTemp["asset_type"] == "Lane4":
        if len(Process.objects.filter(activity_id = pk ,name = saveTemp['name'])) ==0:
            process = Process.objects.get(activity_id=pk, name=saveTemp["old_name"])
            process.name = saveTemp["name"]
            process.save()

            for node in nodeDataArray:
                if node.get("group") != None:
                    if node['group'] == "Lane4" and node['text'] == saveTemp["old_name"]:
                        node['text'] = saveTemp["name"]
