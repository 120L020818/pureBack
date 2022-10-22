import json
from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
def self_controller(request):
    print('已接收到self页面的请求')

    req = json.loads(request.body)
    username=req['username']
    li = list(userTable.objects.filter(UserName=username))
    sex = True if(li[0].Sex=='1')else False
    birthday = li[0].Birthday
    phone=li[0].Phone
    email=li[0].Email
    regDay=li[0].regDay
    cerHave=True
    if True:
        return JsonResponse({
            "success": True,
            "username":username,
            "sex":sex,
            "birthday":birthday,
            "phone":phone,
            "email":email,
            "regDay":regDay,
            "cerHave":cerHave,
        })
    else :
        return JsonResponse({
            "success": False,
        })

