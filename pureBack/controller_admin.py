import json
import sys

from django.http import JsonResponse
import django.utils.timezone as timezone

import base64
import json

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import time,datetime
from Crypto.Signature import PKCS1_v1_5

from vuedata.models import applyTable, certTable, crlTable
from . import controller_logger
from . import http_crypto_helper
from django.http import HttpResponse


def generate_certificate(request):
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)

    ID = req['ID']
    origin = applyTable.objects.filter(RegistrationNumber=ID)
    li = list(origin)
    target = li[0]

    User = target.UserName

    userpubk = RSA.import_key(target.PublicKey)

    nowtime = target.StartTime.strftime("%Y-%m-%d")
    expiretime =target.EndTime.strftime("%Y-%m-%d")

    justicenumber = target.RegistrationNumber

    serialNumber = target.SerialNumber

    hardcore = serialNumber + expiretime + userpubk.exportKey().decode()  # 代签信息

    hash_object2 = SHA256.new()
    hash_object2.update(hardcore.encode('utf-8'))

    f = open('keys/adminprivate.pem', 'r')
    adminprivk = RSA.import_key(f.read())

    signer = PKCS1_v1_5.new(adminprivk)
    signature = signer.sign(hash_object2)
    result = base64.b64encode(signature)
    result = result.decode('utf-8')

    data = json.dumps({'Serial Number': serialNumber, 'Skyrim CA System': 'www.Skyrim.com',
                       'Sign Algorithm': 'sha256+RSA', 'Valid Time From': nowtime,
                       'Valid Time to': expiretime,
                       'User': User, 'User Publickey': userpubk.export_key().decode(),
                       'Sign': result})
    f3 = open(serialNumber + '.json', 'w', encoding='utf-8', newline='')
    json.dump(data, f3)


def applyadmin_controller(request):
    print("已收到applyadmin页面的请求")

    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)

    li = list(applyTable.objects.filter())
    data = []
    for item in li:
        tempdata = {}
        tempdata['authority'] = item.Organization
        tempdata['ID'] = item.RegistrationNumber
        tempdata['username'] = item.JuridicalPerson
        tempdata['chargename'] = item.ChargePerson
        tempdata['chargephone'] = item.ChargePhone
        tempdata['expiretime'] = item.EndTime.__str__()
        data.append(tempdata)

    mydict={"data":data}
    return HttpResponse(helper.encrypt_response_data({
        "success": True,
        "data": mydict,
    }))


def applyadminpass_controller(request):
    print("已收到applyadminpass请求")

    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    ID = req['ID']
    origin = applyTable.objects.filter(RegistrationNumber=ID)
    li = list(origin)
    target = li[0]

    flag=0
    origin2 = certTable.objects.filter(RegistrationNumber=ID)
    li2 = list(origin2)
    if len(li2)>0:
        flag=1
        target2 = li2[0]

    if flag==0:
        data = certTable(RegistrationNumber=target.RegistrationNumber, SerialNumber=target.SerialNumber,
                         Organization=target.Organization,
                         StartTime=target.StartTime, EndTime=target.EndTime, JuridicalPerson=target.JuridicalPerson,
                         ChargePerson=target.ChargePerson, ChargePhone=target.ChargePhone,
                         UserName=target.UserName, PublicKey=target.PublicKey, CertPathName='')
        data.save()
        generate_certificate(request)
    origin.delete()
    logger = controller_logger.logger2
    logger.info(f'[通过]:admin')
    return HttpResponse(helper.encrypt_response_data({
            "success": True,
        }))


def applyadminrefuse_controller(request):
    print("已收到applyadminrefuse请求")
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    print(req)
    print(req)
    ID = req['ID']
    print(ID)
    origin = applyTable.objects.filter(RegistrationNumber=ID)
    li = list(origin)
    target = li[0]
    data = crlTable(SerialNumber=target.SerialNumber, Organization=target.Organization, RevokeTime=timezone.now())
    data.save()
    origin.delete()
    logger = controller_logger.logger2
    logger.info(f'[拒绝]:admin')
    return JsonResponse({
        "success": True,
    })


def isvalidlistadmin_controller(request):
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    print(req)

    print("已收到isvalidlistadmin请求")
    li = list(certTable.objects.filter())
    print(li)
    data = []
    for item in li:
        tempdata = {}
        tempdata['authority'] = item.Organization
        tempdata['ID'] = item.RegistrationNumber
        tempdata['username'] = item.JuridicalPerson
        tempdata['chargename'] = item.ChargePerson
        tempdata['chargephone'] = item.ChargePhone
        tempdata['expiretime'] = item.EndTime.__str__()
        data.append(tempdata)

    mydict = {"data": data}
    # print(req)
    return HttpResponse(helper.encrypt_response_data({
        "success": True,
        "data": mydict,
    }))

def deleteadmin_controller(request):
    print("已收到deleteadmin请求")
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

    print(ID)
    origin = certTable.objects.filter(SerialNumber=ID)
    li = list(origin)
    flag = 0
    if len(li) > 0:
        flag = 1
    target=''
    if flag == 1:
        target = li[0]
        data = crlTable(SerialNumber=target.SerialNumber, Organization=target.Organization, RevokeTime=timezone.now())
        origin.delete()
        data.save()

    if flag == 1 and flag1==1:
        logger = controller_logger.logger2
        logger.info(f'[撤销]:admin    {target.SerialNumber}')
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
        }))

    else:
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))
