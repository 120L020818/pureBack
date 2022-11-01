import json
import sys

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from loguru import logger
from django.http import FileResponse
from vuedata.models import certTable
from . import controller_logger
from . import http_crypto_helper

def download_controller(request):
    print("已收到download页面的请求")
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    ID = req['SerialNumber']
    username=req['username']
    li = list(certTable.objects.filter(SerialNumber=ID))
    flag=0
    if(len(li)>0):
        flag=1
    if flag==1:
        logger = controller_logger.logger2
        logger.info(f'[下载]:{username}')
        f = open(ID+'.json', 'rb')
        # logger.info(f'[下载生成器]:{username}')
        return FileResponse(f)
