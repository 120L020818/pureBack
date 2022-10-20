import json
import sys

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from loguru import logger
from django.http import FileResponse

def cadelete_controller(request):
    print("已收到cadelete页面的请求")
    # req = json.loads(request.body)
    # to_addr1 = req['username']
    # to_addr2 = req['authority']
    # to_addr3 = req['justiceID']
    # to_addr4 = req['admin']
    # to_addr5 = req['adminphone']
    # to_addr6 = req['years']
    # to_addr7 = req['publickey']
    return JsonResponse({
        "success": True,
    })


