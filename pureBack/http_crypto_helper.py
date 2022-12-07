import os
import json
import base64
from . import settings
from . import crypto_helper
import hashlib
# .aes_encrypt, aes_decrypt, rsa_decrypt

class HttpCryptoHelper:
    def __init__(self):
        self.aes_key: bytes = b""
        self.aes_iv: bytes = b""

    def decrypt_request_data(self, encrypted_request):
        sk: bytes = b""
        with open(os.path.join(settings.BASE_DIR, "keys/adminprivate.pem"), "br") as f:
            sk = f.read()

        aes_key: bytes = crypto_helper.rsa_decrypt(sk, base64.b64decode(encrypted_request["ksCipher"]))
        aes_iv: bytes =crypto_helper.rsa_decrypt(sk, base64.b64decode(encrypted_request["ivCipher"]))

        self.aes_key = aes_key
        self.aes_iv = aes_iv

        return json.loads(crypto_helper.aes_decrypt(
            aes_key, aes_iv, base64.b64decode(encrypted_request["bodyCipher"])))

    def encrypt_response_data(self, response_data) -> str:
        if self.aes_key == b"" or self.aes_iv == b"":
            return ""

        response_str = json.dumps(response_data, ensure_ascii=False)
        encrypted_bytes = crypto_helper.aes_encrypt(self.aes_key,
                                      self.aes_iv,
                                      response_str.encode(encoding="UTF-8"))
        return base64.b64encode(encrypted_bytes).decode("UTF-8")

    def dec_vrfy_data(self, request_params) -> bool:
        request_params_mac = request_params['resmac']
        request_params = request_params['data']
        vrfy = hashlib.new('sha1', request_params['bodyCipher'].encode('utf-8'))
        flag = 0
        if vrfy.hexdigest() == request_params_mac['mac']:
            flag = 1
        if flag == 1:
                return True
        else:
                return False
