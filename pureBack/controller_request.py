import json
from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import certTable
def request_controller(request):
    req = json.loads(request.body)
    ID=req['justiceID']
    print('已接收到request页面的请求')
    li = list(certTable.objects.filter(RegistrationNumber=ID))
    flag=0
    if len(li)>0:
        flag=1
    if flag:
        return JsonResponse({
            "success": True,
            "SerialNumber":li[0].SerialNumber,
        })
    else :
        return JsonResponse({
            "success": False,
        })

