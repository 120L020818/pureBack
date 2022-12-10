import json
import sys
from django.http import HttpResponse
from . import http_crypto_helper

from vuedata.models import certTable
from . import controller_logger

def isvalid_controller(request):
    print("已收到isvalid页面的请求")
    request_params = json.loads(request.body.decode("utf-8"))
    req = 0
    helper = http_crypto_helper.HttpCryptoHelper()
    print(request_params)
    flag1 = 0
    if helper.dec_vrfy_data(request_params):
        request_params_data = request_params['data']
        req = helper.decrypt_request_data(request_params_data)
        flag1 = 1

    ID=req['SerialNumber']
    username=req['username']
    print(ID)
    li = list(certTable.objects.filter(SerialNumber=ID))
    flag = 0
    if len(li) > 0:
        flag = 1
    if flag==1 and flag1==1:

        logger = controller_logger.logger2
        logger.info(f'[查询]:{username}')

        return HttpResponse(helper.encrypt_response_data({
            "success": True,
        }))
    else :
        logger = controller_logger.logger2
        logger.info(f'[查询失败]:{username}')
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))

def nomac_controller(request):
    print("已收到isvalid_nomac页面的请求")
    request_params = json.loads(request.body.decode("utf-8"))
    print(request_params)
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    print(req)
    ID=req['SerialNumber']
    # username=req['username']
    print(ID)
    li = list(certTable.objects.filter(SerialNumber=ID))
    flag = 0
    if len(li) > 0:
        flag = 1
    if flag==1:

        logger = controller_logger.logger2
        # logger.info(f'[查询]:{username}')

        return HttpResponse(helper.encrypt_response_data({
            "success": True,
        }))
    else :
        logger = controller_logger.logger2
        # logger.info(f'[查询失败]:{username}')
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))

