import json
import sys

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from vuedata.models import userTable
from . import controller_logger, http_crypto_helper
import bcrypt


def login_controller(request):
    request_params = json.loads(request.body.decode("utf-8"))
    req = 0
    helper = http_crypto_helper.HttpCryptoHelper()
    print(request_params)
    flag2 = 0
    if helper.dec_vrfy_data(request_params):
        request_params_data = request_params['data']
        req = helper.decrypt_request_data(request_params_data)
        flag2 = 1

    username = req['username']
    password = req['password']
    print(username)
    print(password)

    li = list(userTable.objects.filter(UserName=username))
    flag1 = 0
    flag = 0
    isAdmin = False

    if len(li) > 0:
        flag1 = 1
    if flag1 == 1:
        nPassword = password.encode()
        prePassword = li[0].Password
        # salt=li[0].Salt

        if bcrypt.checkpw(nPassword, prePassword):
            print("密码正确")
            flag = 1
        if username == "admin":
            isAdmin = True

    logger = controller_logger.logger

    if flag == 1 and flag2 == 1:
        logger.info(f'[登陆]:{username}')
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
            "isAdmin": isAdmin
        }))
    else:
        logger.info(f'[登陆失败]')
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))


def login_out(request):
    request_params = json.loads(request.body.decode("utf-8"))
    req = 0
    helper = http_crypto_helper.HttpCryptoHelper()
    print(request_params)
    flag = 0
    if helper.dec_vrfy_data(request_params):
        request_params_data = request_params['data']
        req = helper.decrypt_request_data(request_params_data)
        flag = 1

    username = req['username']
    logger = controller_logger.logger
    logger.info(f'[下线]:{username}')
    if flag==1:
        return HttpResponse(helper.encrypt_response_data({
                "success": True,
            }))
