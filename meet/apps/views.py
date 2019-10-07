from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from apps import models
import datetime
import json


class LoginForm(Form):
    username = fields.CharField(
        max_length=8,
        required=True,
        error_messages={
            "max_length":"用户名长度不能大于8位",
            "required":"用户名不能为空",
        },
        # label="用户名",
        # label_suffix=":",
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"username","id":"username"})
    )
    password = fields.CharField(
        max_length=8,
        min_length=3,
        required=True,
        error_messages={
            "max_length":"密码长度不能大于8位",
            "min_length":"密码长度不能小于3位",
            "required":"密码不能为空",
        },
        # label="密码",
        # label_suffix=":",
        widget=widgets.PasswordInput(attrs={"class":"form-control","placeholder":"password","id":"password"}))
def login(request):
    if request.method =="GET":
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = models.UserInfo.objects.filter(**form.cleaned_data).first()
            if user:
                request.session["userinfo"]={"id":user.id,"name":user.username}
                return redirect("/index/")
                # cookie的方式设置
                # obj.set_cookie("name","zzz")
                # obj.set_signed_cookie("id",user.id,salt="aaaa")
                # obj.set_signed_cookie("id1",user.id)
                # return obj
        else:
            form.add_error('password','密码错误')
            return render(request,"login.html",{"form":form})
    return render(request, "login.html", {"form": form})


def index(request):
    metting_list = models.ReserveRecord.time1
    # print(metting_list)
    return render(request,"index.html",{"metting_list":metting_list})

def recording(request):
    response = {"status": True, "msg": None, "data": None}
    if request.method == "GET":
        current_data = datetime.datetime.now().date()  #日期类型
        #=======================获取指定日期所有的预定信息=========================
        try:
            ajax_date= request.GET.get("date")  #字符串类型
            # print(ajax_date,"============")
            ajax_date = datetime.datetime.strptime(ajax_date, '%Y-%m-%d').date()
            # print("date....",ajax_date)
            if ajax_date < current_data:
                raise Exception("查询时间不能是以前的时间")
            recording_list = models.ReserveRecord.objects.filter(data=ajax_date)  #查询的这一天的所有的记录
            # print(recording_list,"recording_list")  # [OBJ(1,room_id,user_id.time_id.data),OBJ(2,room_id,user_id.time_id.data)]
            # 吧这样的数据处理成字典的形式，提升查询速度
            # {
            #     1:{   #room_id
            #         2:{"username":2,"user_id":3}  #2表示time_id
            #     }
            # }
            recrding_dict = {}
            for i in recording_list:
               if i.room_id not in recrding_dict:
                    recrding_dict[i.room_id]={i.timeline:{"username":i.user.username,"user_id":i.user_id}}
               else:
                   # recrding_dict[i.room_id][i.timeline] = {i.timeline:{"username":i.user.username,"user_id":i.user_id}}
                   recrding_dict[i.room_id][i.timeline] = {"username":i.user.username,"user_id":i.user_id}
            print('--------',recrding_dict)
            #获取所有的会议室信息
            room_list = models.MeetingRoom.objects.all()
            #===========================生成会议室信息========================
            data = []
            for room in room_list:
                print(room)
                tr = []
                tr.append({"text": room.name, "attrs": {}})
                for tm in models.ReserveRecord.time1:
                    td = {"text": "", "attrs": {"room_id": room.id, "time_id": tm[0]}}
                    if room.id in recrding_dict and tm[0] in recrding_dict[room.id]:
                        #已预订，不确定是谁预定的，还得判断一下
                        td['attrs']['class'] = "chosen"
                        if recrding_dict[room.id][tm[0]]['user_id'] == request.session["userinfo"]["id"]:
                            #如果是自己预定
                            td['text'] = '我'
                        else:
                            #如果是别人预定，加一个disabled属性不可编辑，只有自己的能编辑
                            td['text'] = recrding_dict[room.id][tm[0]]['username']
                            td['attrs']['disable'] = True
                    tr.append(td)
                data.append(tr)
            print('-==========',data)
            response["data"] = data
        except Exception as e:
            response["status"] = True
            response["msg"] = str(e)
    else:
        try:
            current_date = datetime.datetime.now().date()
            ajax_date = request.POST.get("date")
            ajax_date = datetime.datetime.strptime(ajax_date, '%Y-%m-%d').date()
            if ajax_date < current_date:
                 raise Exception("查询时间不是当前的时间")
            post_data = json.loads(request.POST.get("data"))  #由于发过来的数据是字符串，所以要转一下才能是字典
            print(post_data)  #{'ADD': {'1': ['5', '4'], '2': ['4', '7']}, 'DEL': {'2': ['4']}}}
            date = request.POST.get("date")   #获取日期
            # print(date)  #2017-12-12
            # 拿到数据以后
            # 如果time_id在ADD里面有，在Del里面也有值，就删除了，因为数据库里面已经有值了。就直接把add里的和del里的删除就行了
            for room_id ,time_list in post_data["DEL"].items():
                if room_id  not in post_data["ADD"]:
                    continue
                else:
                    for time_id in list(time_list):
                        if time_id in post_data["ADD"][room_id]:
                            post_data["ADD"][room_id].remove(time_id)
                            post_data["DEL"][room_id].remove(time_id)
                # print(post_data)
            #新增数据
            reserverecord_obj_list = []
            for room_id ,time_list in post_data["ADD"].items():
                for time_id in time_list:
                    # models.ReserveRecord.objects.create(room_id=room_id,time_id=time_id,date=date,user=request.session["userinfo"]["id"])
                    obj = models.ReserveRecord(room_id=room_id,timeline=time_id,data=date,user_id=request.session["userinfo"]["id"])
                    reserverecord_obj_list.append(obj)
            models.ReserveRecord.objects.bulk_create(reserverecord_obj_list)

            #删除会议室预定信息
            from django.db.models import Q
            remove_reserverecord = Q()
            for room_id,time_list in post_data["DEL"].items():
                for time_id in time_list:
                    temp = Q()
                    temp.connector = "AND"
                    temp.children.append(("user_id",request.session["userinfo"]["id"]))
                    temp.children.append(("data",date))
                    temp.children.append(("room_id",room_id))
                    temp.children.append(("timeline",time_id))

                    remove_reserverecord.add(temp,"OR")
            if remove_reserverecord:
                print(models.ReserveRecord.objects.filter(remove_reserverecord))
                models.ReserveRecord.objects.filter(remove_reserverecord).delete()
            # print(remove_reserverecord,"remove_reserverecord")
        except Exception as e:
            response["status"] = False
            response["msg"] = str(e)
    return JsonResponse(response)
