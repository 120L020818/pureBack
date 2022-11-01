import json
from django.shortcuts import render
from django.http import JsonResponse
from . import http_crypto_helper
from vuedata.models import certTable
from django.http import HttpResponse

def request_controller(request):
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)

    ID=req['justiceID']
    print('已接收到request页面的请求')
    li = list(certTable.objects.filter(RegistrationNumber=ID))
    print(li)
    flag=0
    if len(li)>0:
        flag=1
    if flag:
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
            "SerialNumber":li[0].SerialNumber,
        }))
    else :
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))

