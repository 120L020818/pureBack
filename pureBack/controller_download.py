import json

from django.http import FileResponse, HttpResponse
from . import controller_logger
from . import http_crypto_helper
from vuedata.models import certTable
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
from Crypto.Signature import PKCS1_v1_5


def isava_controller(request):
    print("已收到isava页面的请求")
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
    ID = req['SerialNumber']
    li = list(certTable.objects.filter(SerialNumber=ID))
    flag = 0
    if (len(li) > 0):
        flag = 1
    print(flag)
    print(flag1)
    if flag == 1 and flag1 == 1:
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
        }))
    else:
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))


def email_controller(request):
    print("已收到email页面的请求")
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
    li = list(certTable.objects.filter(SerialNumber=ID))
    flag = 0
    if (len(li) > 0):
        flag = 1
    data=''
    if flag == 1 and flag1 == 1:
        logger = controller_logger.logger2
        logger.info(f'[信封传输]:{username}')
        try:
            with open(ID + '.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"正常获得证书,证书是:{data}")
        except Exception as e:
            origin = certTable.objects.filter(SerialNumber=ID)
            li = list(origin)
            target = li[0]

            User = target.UserName

            userpubk = RSA.import_key(target.PublicKey)

            nowtime = target.StartTime.strftime("%Y-%m-%d")
            expiretime = target.EndTime.strftime("%Y-%m-%d")

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

            data = {'Serial Number': serialNumber, 'Skyrim CA System': 'www.Skyrim.com',
                    'Sign Algorithm': 'sha256+RSA', 'Valid Time From': nowtime,
                    'Valid Time to': expiretime,
                    'User': User, 'User Publickey': userpubk.export_key().decode(),
                    'Sign': result}
            print(f"初次生成证书,证书是:{data}")
            f3 = open(serialNumber + '.json', 'w', encoding='utf-8', newline='')
            json.dump(data, f3)

    return HttpResponse(helper.encrypt_response_data({
        "certificate": data,
    }))


def download_controller(request):
    print("已收到download页面的请求")
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
    li = list(certTable.objects.filter(SerialNumber=ID))
    flag = 0
    if (len(li) > 0):
        flag = 1
    if flag == 1 and flag1 == 1:
        logger = controller_logger.logger2
        logger.info(f'[下载]:{username}')
        try:
            f = open(ID + '.json', 'rb')
        except Exception as e:
            origin = certTable.objects.filter(SerialNumber=ID)
            li = list(origin)
            target = li[0]

            User = target.UserName

            userpubk = RSA.import_key(target.PublicKey)

            nowtime = target.StartTime.strftime("%Y-%m-%d")
            expiretime = target.EndTime.strftime("%Y-%m-%d")

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

            data = {'Serial Number': serialNumber, 'Skyrim CA System': 'www.Skyrim.com',
                    'Sign Algorithm': 'sha256+RSA', 'Valid Time From': nowtime,
                    'Valid Time to': expiretime,
                    'User': User, 'User Publickey': userpubk.export_key().decode(),
                    'Sign': result}
            f3 = open(serialNumber + '.json', 'w', encoding='utf-8', newline='')
            json.dump(data, f3)
            f = open(ID + '.json', 'rb')

        response = FileResponse(f)
        # response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = f'attachment;filename="{ID}.json"'

        # logger.info(f'[下载生成器]:{username}')
        return response
