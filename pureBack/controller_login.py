import json
from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable

def login_controller(request):
    req = json.loads(request.body)
    username=req['username']
    password=req['password']
    print(username)
    print(password)
    li=list(userTable.objects.filter(UserName=username))
    flag=0
    isAdmin=False
    if li[0].Password==password:
        flag=1
    if username=="admin":
        isAdmin=True

    if flag==1:
        return JsonResponse({
            "success": True,
            "isAdmin":isAdmin
        })
    else :
        return JsonResponse({
            "success": False,
        })

