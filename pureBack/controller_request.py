import json

from django.http import FileResponse, HttpResponse
from . import controller_logger
from . import http_crypto_helper
from vuedata.models import certTable
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
from Crypto.Signature import PKCS1_v1_5

def request_controller(request):
    request_params = json.loads(request.body.decode("utf-8"))
    req = 0
    helper = http_crypto_helper.HttpCryptoHelper()
    print(request_params)
    flag1 = 0
    if helper.dec_vrfy_data(request_params):
        request_params_data = request_params['data']
        req = helper.decrypt_request_data(request_params_data)
        flag1 = 1

    ID=req['justiceID']
    print('已接收到request页面的请求')
    li = list(certTable.objects.filter(RegistrationNumber=ID))
    print(li)
    flag=0
    if len(li)>0:
        flag=1

    if flag and flag1:
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
            "SerialNumber":li[0].SerialNumber,
        }))
    else :
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))

def nomac_controller(request):
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    ID=req['gsNum']

    print('已接收到nomac页面的请求')
    # 查找获取证书信息
    li = list(certTable.objects.filter(RegistrationNumber=ID))
    print(li[0].SerialNumber)
    print(li[0].UserName)
    username=li[0].UserName
    ID=li[0].SerialNumber

    flag0=0
    if len(li)>0:
        flag0=1

    li = list(certTable.objects.filter(SerialNumber=ID))
    flag = 0
    if (len(li) > 0):
        flag = 1
    data = ''

    if flag0 == 1 and flag==1:
        logger = controller_logger.logger2
        logger.info(f'[信封传输]:{username}')
        try:
            # f = open(f'certificate/{ID}.json', 'rb')
            # with open(ID + '.json', 'r', encoding='utf-8') as f:
            with open(f'certificate/{ID}.json', 'r', encoding='utf-8') as f:
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

            data = {'serialNumber': serialNumber, 'skyrimCASystem': 'www.Skyrim.com',
                    'signAlgorithm': 'sha256+RSA', 'validTimeFrom': nowtime,
                    'validTimeto': expiretime,
                    'user': User, 'userPublickey': userpubk.export_key().decode(),
                    'sign': result}
            print(f"初次生成证书,证书是:{data}")
            f3 = open(f'certificate/{serialNumber}.json', 'rb')
            # f3 = open( + '.json', 'w', encoding='utf-8', newline='')
            json.dump(data, f3)

    return HttpResponse(helper.encrypt_response_data(
        data
    ))


