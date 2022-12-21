import hashlib
import json
import requests
from django.http import FileResponse, HttpResponse
from . import controller_logger
from . import http_crypto_helper
from vuedata.models import certTable
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher, AES
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import M2Crypto as m2c


def bank_controller(request):
    print("已收到电商的请求")

    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    encKs = req['encKs']
    print(encKs)
    pi = req['pi']
    oimd = req['oimd']
    ds = req['ds']

    f = open('keys/adminprivate.pem', 'r')
    key = RSA.import_key(f.read())
    print(key.publickey().export_key())
    decrypt_rsa = PKCS1_cipher.new(key)
    aes_key = decrypt_rsa.decrypt(base64.b64decode(encKs), 23333)
    mydata = {
        "aes_key": aes_key.decode('utf-8'),
        "pi": pi,
        "oimd": oimd,
        "ds": ds
    }
    with open("cache/temp.json", 'w', encoding='utf-8', newline='') as f:
        json.dump(mydata, f)

    print(req)
    # res=requests.post(url='http://192.168.0.102:8080/test',
    #               data={"username":"admin"})

    return HttpResponse(helper.encrypt_response_data({
        "success": False,
    }))


def vrfy_controller(request):
    print("已接收到vrfy页面的请求")
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

    if flag1 == 1:
        with open("cache/temp.json", 'r', encoding='utf-8') as f:
            mydata = json.load(f)
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
            "mydata": mydata
        }))
    else:
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))


def log_controller(request):
    print("已接收到res页面的请求")
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    verified = req['verified']
    print(verified)
    mydata = {'verified': verified}
    with open("cache/result.json", 'w', encoding='utf-8') as f:
        json.dump(mydata, f)

    return HttpResponse(helper.encrypt_response_data({
        "success": True,
    }))


def ret_controller(request):
    print("已接收到ret页面的请求")
    request_params = json.loads(request.body.decode("utf-8"))
    helper = http_crypto_helper.HttpCryptoHelper()
    req = helper.decrypt_request_data(request_params)
    with open("cache/result.json", 'r', encoding='utf-8') as f:
        mydata = json.load(f)
        print(mydata)
        print(mydata['verified'])
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
            "mydata": mydata['verified']
        }))
