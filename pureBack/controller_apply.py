import json
import sys

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from loguru import logger
from django.http import FileResponse

def apply_controller(request):
    print("已收到apply页面的请求")
    req = json.loads(request.body)
    to_addr1 = req['username']
    to_addr2 = req['authority']
    to_addr3 = req['justiceID']
    to_addr4 = req['admin']
    to_addr5 = req['adminphone']
    to_addr6 = req['years']
    to_addr7 = req['publickey']
    return JsonResponse({
        "success": True,
    })

def download_genrater(request):
    print("success")

    req = json.loads(request.body)
    # username = req['username']
    f=open('generate.exe','rb')
    # logger.info(f'[下载生成器]:{username}')
    return FileResponse(f)


def download_protector(request):
    print("success")

    req = json.loads(request.body)
    # username = req['username']
    f = open('protect.exe', 'rb')
    # logger.info(f'[下载加密器]:{username}')
    return FileResponse(f)
