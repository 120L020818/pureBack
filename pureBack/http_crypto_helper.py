import os
import json
import base64
from . import settings
from . import crypto_helper

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
