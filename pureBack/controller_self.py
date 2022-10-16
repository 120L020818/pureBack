import json
from django.shortcuts import render
from django.http import JsonResponse

def self_controller(request):
    req = json.loads(request.body)
    print('已接收到self页面的请求')
    if True:
        return JsonResponse({
            "success": True,
            "username":"刻晴",
            "sex":False,
            "birthday":"2001/09/24",
            "phone":"15505589252",
            "email":"835766751@qq.com",
            "regDay":"2022/10/19",
            "cerHave":True,
        })
    else :
        return JsonResponse({
            "success": False,
        })

