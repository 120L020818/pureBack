import json
import sys

from django.shortcuts import render
from django.http import JsonResponse
from vuedata.models import userTable
from loguru import logger
from django.http import FileResponse
import django.utils.timezone as timezone

import base64
import json

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import time,datetime
from Crypto.Signature import PKCS1_v1_5

from vuedata.models import applyTable, certTable, crlTable


def generate_certificate(request):
    req = json.loads(request.body)
    ID = req['ID']
    origin = applyTable.objects.filter(RegistrationNumber=ID)
    li = list(origin)
    target = li[0]

    User = target.UserName
    # userpubk = target.PublicKey
    # print(userpubk)
    # li =userpubk.split(' ')
    # userpubk = li[0] + ' ' + li[1] + ' ' + li[2] + '\n'
    # userpubk += li[3] + '\n'
    # userpubk += li[4] + '\n'
    # userpubk += li[5] + '\n'
    # userpubk += li[6] + '\n'
    # userpubk += li[7] + ' ' + li[8] + ' ' + li[9]
    #
    userpubk = RSA.import_key(target.PublicKey)

    print(type(target.StartTime))
    nowtime = target.StartTime.strftime("%Y-%m-%d")
    print(nowtime)
    expiretime =target.EndTime.strftime("%Y-%m-%d")
    print(expiretime)

    justicenumber = target.RegistrationNumber

    serialNumber = target.SerialNumber

    hardcore = serialNumber + expiretime + userpubk.exportKey().decode()  # 代签信息

    hash_object2 = SHA256.new()
    hash_object2.update(hardcore.encode('utf-8'))

    f = open('adminprivate.pem', 'r')
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
    # print("已收到applyadmin页面的请求")
    # req = json.loads(request.body)
    li = list(applyTable.objects.filter())
    print(li)
    data = []
    for item in li:
        tempdata = {}
        tempdata['authority'] = item.Organization
        tempdata['ID'] = item.RegistrationNumber
        tempdata['username'] = item.JuridicalPerson
        tempdata['chargename'] = item.ChargePerson
        tempdata['chargephone'] = item.ChargePhone
        tempdata['expiretime'] = item.EndTime
        data.append(tempdata)
    # print(req)
    return JsonResponse({
        "success": True,
        "data": data
    })


def applyadminpass_controller(request):
    print("已收到applyadminpass请求")
    req = json.loads(request.body)
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
    return JsonResponse({
        "success": True,
    })


def applyadminrefuse_controller(request):
    print("已收到applyadminrefuse请求")
    req = json.loads(request.body)
    print(req)
    ID = req['ID']
    print(ID)
    origin = applyTable.objects.filter(RegistrationNumber=ID)
    li = list(origin)
    target = li[0]
    data = crlTable(SerialNumber=target.SerialNumber, Organization=target.Organization, RevokeTime=timezone.now())
    data.save()
    origin.delete()
    return JsonResponse({
        "success": True,
    })


def isvalidlistadmin_controller(request):
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
        tempdata['expiretime'] = item.EndTime
        data.append(tempdata)
    # print(req)
    return JsonResponse({
        "success": True,
        "data": data
    })


def isvalidadmin_controller(request):
    print("已收到isvalidadmin请求")
    req = json.loads(request.body)
    print(req)
    ID = req['ID']
    # print(req)
    return JsonResponse({
        "success": True,
    })


def deleteadmin_controller(request):
    print("已收到deleteadmin请求")
    req = json.loads(request.body)
    ID = req['SerialNumber']
    print(ID)
    origin = certTable.objects.filter(SerialNumber=ID)
    li = list(origin)
    flag = 0
    if len(li) > 0:
        flag = 1

    if flag == 1:
        target = li[0]
        data = crlTable(SerialNumber=target.SerialNumber, Organization=target.Organization, RevokeTime=timezone.now())
        origin.delete()
        data.save()

    if flag == 1:
        return JsonResponse({
            "success": True,
        })
    else:
        return JsonResponse({
            "success": False,
        })
