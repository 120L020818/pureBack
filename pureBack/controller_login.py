import json
from django.shortcuts import render
from django.http import JsonResponse
def login_controller(request):
    req = json.loads(request.body)
    username=req['username']
    password=req['password']
    print(username)
    print(password)
    # print(params)
    isAdmin=False
    if True:
        return JsonResponse({
            "success": True,
            "isAdmin":isAdmin
        })
    else :
        return JsonResponse({
            "success": False,
        })

