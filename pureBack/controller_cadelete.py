import json
import sys

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from loguru import logger
from django.http import FileResponse
from vuedata.models import certTable, crlTable
import django.utils.timezone as timezone
from . import controller_logger


def cadelete_controller(request):
    print("已收到cadelete页面的请求")
    req = json.loads(request.body)
    ID = req['SerialNumber']
    username = req['username']
    print(ID)
    origin = certTable.objects.filter(SerialNumber=ID)
    li = list(origin)
    flag = 0
    if len(li) > 0:
        flag = 1
        if li[0].UserName != username:
            flag = 0
    if flag == 1:
        target = li[0]
        data = crlTable(SerialNumber=target.SerialNumber, Organization=target.Organization, RevokeTime=timezone.now())
        origin.delete()
        data.save()

    if flag == 1:
        logger = controller_logger.logger2
        logger.info(f'[撤销]:{username}')
        return JsonResponse({
            "success": True,
        })
    else:
        return JsonResponse({
            "success": False,
        })
