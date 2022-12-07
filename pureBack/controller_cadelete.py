import json

from vuedata.models import certTable, crlTable
import django.utils.timezone as timezone
from . import controller_logger
from . import http_crypto_helper
from django.http import HttpResponse


def cadelete_controller(request):
    print("已收到cadelete页面的请求")
    request_params = json.loads(request.body.decode("utf-8"))
    req = 0
    helper = http_crypto_helper.HttpCryptoHelper()
    print(request_params)
    flag1 = 0
    if helper.dec_vrfy_data(request_params):
        request_params_data = request_params['data']
        req = helper.decrypt_request_data(request_params_data)
        flag1 = 1


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

    if flag == 1 and flag1==1:
        logger = controller_logger.logger2
        logger.info(f'[撤销]:{username}')
        return HttpResponse(helper.encrypt_response_data({
        "success": True,
        "msg": ""
    }))
    else:
        return HttpResponse(helper.encrypt_response_data({
        "success": False,
        "msg": ""
    }))
