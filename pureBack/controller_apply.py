import json
import sys

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from loguru import logger
from django.http import FileResponse

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
