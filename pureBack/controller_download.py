import json


from django.http import FileResponse
from . import controller_logger
from . import http_crypto_helper
from vuedata.models import  certTable
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
from Crypto.Signature import PKCS1_v1_5


def download_controller(request):
    print("已收到download页面的请求")
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    ID = req['SerialNumber']
    username = req['username']
    li = list(certTable.objects.filter(SerialNumber=ID))
    flag = 0
    if (len(li) > 0):
        flag = 1
    if flag == 1:
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

            data = json.dumps({'Serial Number': serialNumber, 'Skyrim CA System': 'www.Skyrim.com',
                               'Sign Algorithm': 'sha256+RSA', 'Valid Time From': nowtime,
                               'Valid Time to': expiretime,
                               'User': User, 'User Publickey': userpubk.export_key().decode(),
                               'Sign': result})
            f3 = open(serialNumber + '.json', 'w', encoding='utf-8', newline='')
            json.dump(data, f3)
            f = open(ID + '.json', 'rb')

        # logger.info(f'[下载生成器]:{username}')
        return FileResponse(f)
