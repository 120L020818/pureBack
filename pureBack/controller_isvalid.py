import json
import sys
from django.http import HttpResponse
from . import http_crypto_helper

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from loguru import logger
from django.http import FileResponse
from vuedata.models import certTable
from . import controller_logger

def isvalid_controller(request):
    print("已收到isvalid页面的请求")
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)

    ID=req['SerialNumber']
    username=req['username']
    print(ID)
    li = list(certTable.objects.filter(SerialNumber=ID))
    flag = 0
    if len(li) > 0:
        flag = 1
    if flag==1:

        logger = controller_logger.logger2
        logger.info(f'[查询]:{username}')

        return HttpResponse(helper.encrypt_response_data({
            "success": True,
        }))
    else :
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))

