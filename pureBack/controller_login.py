import json
import sys

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from loguru import logger
import bcrypt


logger.remove()  # 这里是不让他重复打印
logger.add(sys.stderr,  # 这里是不让他重复打印
           level="INFO"
           )

def login_controller(request):
    req = json.loads(request.body)
    username = req['username']
    password = req['password']
    print(username)
    print(password)
    li = list(userTable.objects.filter(UserName=username))
    flag = 0
    isAdmin = False


    nPassword=password.encode()
    print(nPassword)
    prePassword=li[0].Password
    print(prePassword)
    salt=li[0].Salt
    print(bcrypt.hashpw(nPassword,salt))

    if bcrypt.checkpw(nPassword,prePassword):
        print("密码正确")
        flag = 1
    if username == "admin":
        isAdmin = True

    logger.add('user.log', encoding='utf-8',format="{time}  |   {message}")
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
    logger.info(f'[下线]:{username}')
    return JsonResponse({
        "success": True,
    })


