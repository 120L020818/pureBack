from django.http import FileResponse
from vuedata.models import applyTable
from . import controller_logger

import base64

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import time
from Crypto.Signature import PKCS1_v1_5

import json
from . import http_crypto_helper
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_controller(request):
    request_params = json.loads(request.body.decode("utf-8"))

    helper = http_crypto_helper.HttpCryptoHelper()

    request_data = helper.decrypt_request_data(request_params)

    print(request_data)

    return HttpResponse(helper.encrypt_response_data({
        "success": True,
        "msg": ""
    }))

def apply_controller(request):
    print("已收到apply页面的请求")
    request_params = json.loads(request.body.decode("utf-8"))
    req = 0
    helper = http_crypto_helper.HttpCryptoHelper()
    print(request_params)
    flag1 = 0
    if helper.dec_vrfy_data(request_params):
        request_params_data = request_params['data']
        req = helper.decrypt_request_data(request_params_data)
        flag1 = 1

    print(req)

    to_addr1 = req['juridicalperson']
    to_addr2 = req['authority']
    to_addr3 = req['justiceID']
    to_addr4 = req['admin']
    to_addr5 = req['adminphone']
    to_addr6 = req['years']
    to_addr7 = req['publickey']
    to_addr8 = req['username']

    li=to_addr7.split(' ')
    to_addr7=li[0]+' '+li[1]+' '+li[2]+'\n'
    for i in range(3,len(li)-3):
        to_addr7+=li[i]+'\n'
    to_addr7+=li[-3]+' '+li[-2]+' '+li[-1]

    userpubk = RSA.import_key(to_addr7)
    print(len(userpubk.exportKey().decode()))
    nowtime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    temp = nowtime.split('-')
    temp[0] = str(int(temp[0]) + int(to_addr6))
    expiretime = temp[0] + '-' + temp[1] + '-' + temp[2]
    justicenumber = to_addr3
    data = nowtime + justicenumber
    hash_object = SHA256.new()
    hash_object.update(data.encode('utf-8'))
    serialNumber = hash_object.hexdigest()
    hardcore = serialNumber + expiretime + userpubk.exportKey().decode()  # 代签信息
    hash_object2 = SHA256.new()
    hash_object2.update(hardcore.encode('utf-8'))
    f = open('keys/adminprivate.pem', 'r')
    adminprivk = RSA.import_key(f.read())

    signer = PKCS1_v1_5.new(adminprivk)
    signature = signer.sign(hash_object2)
    result = base64.b64encode(signature)
    result = result.decode('utf-8')


    target=applyTable(RegistrationNumber=to_addr3,SerialNumber=serialNumber,Organization=
                      to_addr2,StartTime=nowtime,EndTime=expiretime,JuridicalPerson=to_addr1,
                      ChargePerson=to_addr4,ChargePhone=to_addr5,PublicKey=to_addr7,UserName=to_addr8)
    target.save()

    print(req)
    logger = controller_logger.logger2
    logger.info(f'[申请]:{to_addr1}')
    if flag1==1:
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
            "msg": ""
        }))

def download_genrater(request):
    print("success")

    req = json.loads(request.body)
    username = req['username']
    f=open('generate.exe','rb')
    logger = controller_logger.logger2
    logger.info(f'[申请]:{username}')
    # logger.info(f'[下载生成器]:{username}')
    return FileResponse(f)


def download_protector(request):
    print("success")

    req = json.loads(request.body)
    username = req['username']
    f = open('protect.exe', 'rb')
    logger = controller_logger.logger2
    logger.info(f'[下载加密器]:{username}')
    return FileResponse(f)
