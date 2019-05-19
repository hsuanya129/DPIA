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
activityID = 0
userid = 0

def index(request):
    return render(request,'team/home.html/',locals())

def login_sign(request):
    global activityID,userid
    if request.method == "POST":
        if 'login' in request.POST:#一個表單兩個action時要用到 此為按下登入時觸發的action
            account = request.POST['account']
            password = request.POST['password']
            user = User.objects.filter(account=account,password=password)

            if len(user) != 0:
                user = User.objects.get(account=account,password=password)
                userid = user.id
                user_has_activity = UserHasActivity.objects.filter(user_id = userid) #擷取出此user有的activity
                # activityID = UserHasActivity.objects.filter(user_id = userid)
                # print(activityID)
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
                    activity_id=activityID #test id 
                )

        if questionary_type_id == '1':

            return HttpResponseRedirect(base_url + 'team/stakeholder')

        elif questionary_type_id == '3' or '2':

            return render(request, 'team/stakeholder.html', locals())
        # if questionary_type_id == '1' or '2':

        #     return HttpResponseRedirect(base_url + 'team/questionary/' + str(int(questionary_type_id)+1))

        # elif questionary_type_id == '3':

        #     return render(request,'team/stakeholder.html', locals())


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
        Stakeholder.objects.create(name=name, role=role, email=email, part=part, feedback=feedback, activity_id=activityID)
        return HttpResponseRedirect(base_url + 'team/dataflow')
    return render(request, 'team/stakeholder.html', locals())
def new(request):
    global userid,activityID
    # print(userid)
    user_pk = userid #it's for user's id
    if request.method == 'POST':
        name = request.POST.get('pia_name','')
        piam_name = request.POST.get('piam_name','')
        piam_email = request.POST.get('piam_email','')
        activity_manager_name = request.POST.get('activitym_name','')
        activity_manager_email = request.POST.get('activitym_email','')
        today = datetime.date.today()
        description = request.POST.get('description','')
        new_pia = Activity.objects.create(name=name,pia_manager_name=piam_name,pia_manager_email=piam_email,activity_manager_name=activity_manager_name,activity_manager_email=activity_manager_email,date=today,description=description)
        UserHasActivity.objects.create(user_id=user_pk,activity_id=new_pia.id)
        activityID = new_pia.id
        # print(activityID)
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
        user = User.objects.create(name=name,account=account, password=password,permission_level=1)
        return HttpResponseRedirect('/team/')
    return HttpResponseRedirect('/team/')

def dataflow(request):
    pk =activityID
    swimlane_objects = Swimlane.objects.filter(activity_id=pk)
    if len(swimlane_objects) == 0:
        Swimlane.objects.create(activity_id= pk)

    return render(request, 'team/dataflow.html')

def dataflow_saveLane(request):
    pk =activityID

    swimlane_object_post = Swimlane.objects.get(activity_id=pk)
    data_text = request.POST.get('postdata')
    data_json = json.loads(data_text)
    swimlane_object_post.swimlane_json = data_json  
    swimlane_object_post.save()

    return render(request, 'team/dataflow.html')


def dataflow_get(request):
    pk=activityID
    swimlane_object_get = Swimlane.objects.get(activity_id=pk)
    if json.dumps(swimlane_object_get.swimlane_json) == "{}":
        swimlane_object_one = Swimlane.objects.get(activity_id=1)
        swimlane_object_get.swimlane_json = swimlane_object_one.swimlane_json
        swimlane_object_get.save()
        Process.objects.create(activity_id=pk,name="Collect")
        Process.objects.create(activity_id=pk,name="Store")
        Process.objects.create(activity_id=pk,name="Use")
        Process.objects.create(activity_id=pk,name="Transfer")
        Process.objects.create(activity_id=pk,name="Delete")
    return JsonResponse(swimlane_object_get.swimlane_json)

#收到由dataflow.html的post請求, 對應其post資訊中的event, 分流至相應事件(新增/刪除/修改 節點)的方法
def dataflow_saveTemp(request):
    pk=activityID
    saveTemp = request.POST.get('postdata')
    saveTemp = json.loads(saveTemp)
    print(saveTemp)

    if saveTemp["event"]=="addNode":
        addNode(saveTemp,pk)
    elif saveTemp["event"]=="removeNode":
        removeNode(saveTemp,pk)
    elif saveTemp["event"]=="rename" :
        renameNode(saveTemp,pk)
    elif saveTemp["event"]=="addValue" :
        addValue(saveTemp,pk)

    return render(request, 'team/dataflow.html')

#節點新增時所啟動的方法: 將新增的節點, 新增與之process對應關係
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

#節點刪除時所啟動的方法: 將刪除的節點, 刪除與之process對應關係
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

#節點重新命名時 所啟動的方法: 將所改變的節點名字存入資料庫
def renameNode(saveTemp,pk):
    if saveTemp['old_name'] == saveTemp['name']:
        print("OLD NAME = NEW NAME RETURN")
        return

    if saveTemp["asset_type"] =="Lane1":
        process = Process.objects.get(activity_id=pk, name=saveTemp['process'])
        participant_old = Participant.objects.get(activity_id=pk, name=saveTemp['old_name'])
        if len(ProcessHasParticipant.objects.filter(participant_id=participant_old.id))==1: #舊的name只有一個物件
            if len(Participant.objects.filter(activity_id=pk, name=saveTemp['name'])) ==0: #新的name尚未有物件
                participant_old.name = saveTemp['name']
                participant_old.save()
                

            elif len(Participant.objects.filter(activity_id=pk, name=saveTemp['name'])) ==1: #新的name已有物件
                participant_new = Participant.objects.get(activity_id=pk, name=saveTemp['name'])
                participant_old.delete()
                ProcessHasParticipant.objects.create(participant_id=participant_new.id,process_id=process.id)
                

        elif len(ProcessHasParticipant.objects.filter(participant_id=participant_old.id))!=1: #舊的name不只有一個物件
            if len(Participant.objects.filter(activity_id=pk, name=saveTemp['name'])) ==0: #新的name尚未有物件
                Participant.objects.create(activity_id=pk, name=saveTemp['name'])
                participant_new = Participant.objects.get(activity_id=pk, name=saveTemp['name'])
                processHasParticipant_old = ProcessHasParticipant.objects.get(process_id=process.id,participant_id=participant_old.id)
                processHasParticipant_old.delete()
                ProcessHasParticipant.objects.create(process_id=process.id,participant_id=participant_new.id)
                

            elif len(Participant.objects.filter(activity_id=pk, name=saveTemp['name'])) ==1: #新的name已有物件
                participant_new = Participant.objects.get(activity_id=pk, name=saveTemp['name'])
                processHasParticipant_old = ProcessHasParticipant.objects.get(process_id=process.id,participant_id=participant_old.id)
                processHasParticipant_old.delete()
                ProcessHasParticipant.objects.create(process_id=process.id,participant_id=participant_new.id)
                

    elif saveTemp["asset_type"] == "Lane2":
        process = Process.objects.get(activity_id=pk, name=saveTemp['process'])
        system_old = System.objects.get(activity_id=pk, name=saveTemp['old_name'])
        if len(ProcessHasSystem.objects.filter(system_id=system_old.id))==1: #舊的name只有一個物件
            if len(System.objects.filter(activity_id=pk, name=saveTemp['name'])) ==0: #新的name尚未有物件
                system_old.name = saveTemp['name']
                system_old.save()
                

            elif len(System.objects.filter(activity_id=pk, name=saveTemp['name'])) ==1: #新的name已有物件
                system_new = System.objects.get(activity_id=pk, name=saveTemp['name'])
                system_old.delete()
                ProcessHasSystem.objects.create(system_id=system_new.id,process_id=process.id)
                

        elif len(ProcessHasSystem.objects.filter(system_id=system_old.id))!=1: #舊的name不只有一個物件
            if len(System.objects.filter(activity_id=pk, name=saveTemp['name'])) ==0: #新的name尚未有物件
                System.objects.create(activity_id=pk, name=saveTemp['name'])
                system_new = System.objects.get(activity_id=pk, name=saveTemp['name'])
                processHasSystem_old = ProcessHasSystem.objects.get(process_id=process.id,system_id=system_old.id)
                processHasSystem_old.delete()
                ProcessHasSystem.objects.create(process_id=process.id,system_id=system_new.id)
                

            elif len(System.objects.filter(activity_id=pk, name=saveTemp['name'])) ==1: #新的name已有物件
                system_new = System.objects.get(activity_id=pk, name=saveTemp['name'])
                processHasSystem_old = ProcessHasSystem.objects.get(process_id=process.id,system_id=system_old.id)
                processHasSystem_old.delete()
                ProcessHasSystem.objects.create(process_id=process.id,system_id=system_new.id)

    elif (saveTemp["asset_type"]=="Lane3" or saveTemp["asset_type"]=="Lane5") :
        print("it's pii")
        process = Process.objects.get(activity_id=pk, name=saveTemp['process'])
        pii_old = Pii.objects.get(activity_id=pk, name=saveTemp['old_name'])
        if len(ProcessHasPii.objects.filter(pii_id=pii_old.id))==1: #舊的name只有一個物件
            if len(Pii.objects.filter(activity_id=pk, name=saveTemp['name'])) ==0: #新的name尚未有物件
                pii_old.name = saveTemp['name']
                pii_old.save()
                

            elif len(Pii.objects.filter(activity_id=pk, name=saveTemp['name'])) ==1: #新的name已有物件
                pii_new = Pii.objects.get(activity_id=pk, name=saveTemp['name'])
                pii_old.delete()
                ProcessHasPii.objects.create(pii_id=pii_new.id,process_id=process.id)
                
        elif len(ProcessHasPii.objects.filter(pii_id=pii_old.id))!=1: #舊的name不只有一個物件
            if len(Pii.objects.filter(activity_id=pk, name=saveTemp['name'])) ==0: #新的name尚未有物件
                Pii.objects.create(activity_id=pk, name=saveTemp['name'])
                pii_new = Pii.objects.get(activity_id=pk, name=saveTemp['name'])
                processHasPii_old = ProcessHasPii.objects.get(process_id=process.id,pii_id=pii_old.id)
                processHasPii_old.delete()
                ProcessHasPii.objects.create(process_id=process.id,pii_id=pii_new.id)

            elif len(Pii.objects.filter(activity_id=pk, name=saveTemp['name'])) ==1: #新的name已有物件
                pii_new = Pii.objects.get(activity_id=pk, name=saveTemp['name'])
                processHasPii_old = ProcessHasPii.objects.get(process_id=process.id,pii_id=pii_old.id)
                processHasPii_old.delete()
                ProcessHasPii.objects.create(process_id=process.id,pii_id=pii_new.id)

    elif saveTemp["asset_type"] == "Lane4":
        process_old = Process.objects.get(activity_id = pk , name = saveTemp['old_name'])
        process_old.name = saveTemp['name']
        process_old.save()

def addValue(saveTemp,pk):
    pii=Pii.objects.get(activity_id=pk, name=saveTemp["name"])
    pii.value=saveTemp["value"]
    pii.save()

def evaluation(request):
    pk=3

    #在此收到evaluation頁面的post請求，並將頁面中使用者填入的資料輸入至資料庫中
    if request.method == "POST":

        probability_list=list()
        description_list=list()
        applicable_list=list()

        #將各evaluation item中的資料匯入成list 使之方便存入至資料庫
        for group in Evaluation.objects.filter(activity_id=pk):
            applicable_list.append(request.POST.get('applicable'+ str(group.id)))

            for item in EvaluationItem.objects.filter(evaluation_id=group.id):
                probability_list.append(request.POST.get('probability'+ str(item.id)))
                description_list.append(request.POST.get('description'+ str(item.id)))


        #以上方list所存之資料為依據 匯入至資料庫
        i=0
        j=0
        for group in Evaluation.objects.filter(activity_id=pk):
            print(applicable_list[i])
            if applicable_list[i]=="on":
                group.applicable=True
                group.save()

            for item in EvaluationItem.objects.filter(evaluation_id=group.id):
                item.probability=probability_list[j]
                item.description=description_list[j]
                item.save()
                j+=1
            i+=1
        return HttpResponseRedirect('/team/risk_mapping')

    #在此創立evalation物件
    if request.method=="GET":
        process_all = Process.objects.filter(activity_id=pk)

        #若此activity已有evaluation物件 則刪除原有物件 在下方程式碼中recreate
        if len(Evaluation.objects.filter(activity_id = pk))>0:
            for item in Evaluation.objects.filter(activity_id = pk):
                item.delete()

        #在此建立evaluation_item物件
        if len(Evaluation.objects.filter(activity_id = pk))==0:
            for process in process_all:
                for process_has_pii in ProcessHasPii.objects.filter(process_id = process.id):
                    pii = Pii.objects.get(id =process_has_pii.pii_id )
                    for process_has_system in ProcessHasSystem.objects.filter(process_id = process.id):
                        system = System.objects.get(id=process_has_system.system_id)
                        evaluation = Evaluation.objects.create(activity_id=pk,pii_id=pii.id,system_id = system.id,value=pii.value,process_id=process.id)
                        EvaluationItem.objects.create(risk="Disappearance of Pii",evaluation_id=evaluation.id)
                        EvaluationItem.objects.create(risk="Illeagal of uasge",evaluation_id=evaluation.id)
                        EvaluationItem.objects.create(risk="Unwanted modified Pii",evaluation_id=evaluation.id)

                    for process_has_participant in ProcessHasParticipant.objects.filter(process_id = process.id):
                        participant = Participant.objects.get(id=process_has_participant.participant_id)
                        evaluation = Evaluation.objects.create(activity_id=pk,pii_id=pii.id,participant_id = participant.id,value=pii.value,process_id=process.id)
                        EvaluationItem.objects.create(risk="Disappearance of Pii",evaluation_id=evaluation.id)
                        EvaluationItem.objects.create(risk="Illeagal of uasge",evaluation_id=evaluation.id)
                        EvaluationItem.objects.create(risk="Unwanted modified Pii",evaluation_id=evaluation.id)

        context ={
            'process_all':process_all,
            'process_has_pii_all':ProcessHasPii.objects.all(),
            'process_has_participant':ProcessHasParticipant.objects.all(),
            'evaluation_all':Evaluation.objects.filter(activity_id = pk),
            'evaluation_item_all':EvaluationItem.objects.all()
        }      

        return render(request,'team/evaluation.html',context)


def risk_mapping(request):
    pk=3
    context ={
        'evaluation_item_all':EvaluationItem.objects.all(),
        'evaluation_all':Evaluation.objects.filter(activity_id = pk,applicable=True)
    }
    return render(request,'team/risk_mapping.html',context)   
def choose_pia(request):
    if request.method == "POST":
        data = request.POST.get('data')
        print(data)
        json_data = json.loads(data)
        pk = json_data['takedValue']
        pkk = int(float(pk))
        activityID = pkk
        print(pkk)
        print(activityID)
        activity_project = Activity.objects.filter(id = activityID)
        # activity_project = Activity.objects.filter(id = activityID)
        return render(request,'team/pia_examine.html/',locals())
def pia_examine(request):
    # user_has_activity = Activity.objects.filter(id = activityID)
    return render(request, 'team/pia_examine.html',locals())



