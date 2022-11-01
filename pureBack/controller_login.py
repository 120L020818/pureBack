import json
import sys

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from . import controller_logger
import bcrypt


def login_controller(request):
    req = json.loads(request.body)
    username = req['username']
    password = req['password']
    print(username)
    print(password)
    li = list(userTable.objects.filter(UserName=username))
    flag1 = 0
    flag=0
    isAdmin = False

    if len(li) > 0:
        flag1 = 1
    if flag1==1:
        nPassword=password.encode()
        prePassword=li[0].Password
    # salt=li[0].Salt

        if bcrypt.checkpw(nPassword,prePassword):
            print("密码正确")
            flag = 1
        if username == "admin":
            isAdmin = True

    logger=controller_logger.logger

    if flag == 1:
        logger.info(f'[登陆]:{username}')
        return JsonResponse({
            "success": True,
            "isAdmin": isAdmin
        })
    else:
        logger.info(f'[登陆失败]')
        return JsonResponse({
            "success": False,
        })


def login_out(request):
    req = json.loads(request.body)
    username = req['username']
    logger=controller_logger.logger
    logger.info(f'[下线]:{username}')
    return JsonResponse({
        "success": True,
    })


