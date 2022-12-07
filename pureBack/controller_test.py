import hashlib
import json
from . import http_crypto_helper
from django.http import HttpResponse

def test_controller(request):
    request_params = json.loads(request.body.decode("utf-8"))

    helper = http_crypto_helper.HttpCryptoHelper()
    print(request_params)
    flag=0
    if helper.dec_vrfy_data(request_params):
        request_params_data=request_params['data']
        req = helper.decrypt_request_data(request_params_data)
        flag=1

        print(req)
    if flag==1:
        return HttpResponse(helper.encrypt_response_data({
            "success": True,
        }))
    else:
        return HttpResponse(helper.encrypt_response_data({
            "success": False,
        }))
