import json

from vuedata.models import userTable
from . import http_crypto_helper
from django.http import HttpResponse

def self_controller(request):
    print('已接收到self页面的请求')
    request_params = json.loads(request.body.decode("utf-8"))
    req = 0
    helper = http_crypto_helper.HttpCryptoHelper()
    print(request_params)
    flag1 = 0
    if helper.dec_vrfy_data(request_params):
        request_params_data = request_params['data']
        req = helper.decrypt_request_data(request_params_data)
        flag1 = 1

    username=req['username']
    li = list(userTable.objects.filter(UserName=username))

    flag = 0
    if len(li) > 0:
        flag = 1
    sex=''
    birthday=''
    phone=''
    email=''
    regDay=''
    cerHave=''
    if flag==1:
        sex = True if(li[0].Sex=='1')else False
        birthday = li[0].Birthday.__str__()
        phone=li[0].Phone
        email=li[0].Email
        regDay=li[0].regDay.__str__()
        cerHave=True
    # print(sex,type(sex))
    # print(birthday,type(birthday))
    # print(phone,type(phone))
    # print(email,type(email))
    # print(regDay,type(regDay))
    # print(cerHave,type(cerHave))
    if flag==1 and flag1==1:
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
            "username": username,
            "sex": sex,
            "birthday": birthday,
            "phone": phone,
            "email": email,
            "regDay": regDay,
            "cerHave": cerHave,
        }))
    else :
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
            "msg": ""
        }))
