import json
import sys

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from loguru import logger
from django.http import FileResponse
from vuedata.models import certTable
from . import controller_logger

def isvalid_controller(request):
    print("已收到isvalid页面的请求")
    req = json.loads(request.body)
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

        return JsonResponse({
            "success": True,
        })
    else :
        return JsonResponse({
            "success": False,
        })

