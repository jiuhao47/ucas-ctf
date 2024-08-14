#!/usr/bin/env python3

import os
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor

class AES_OFB:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
    def encrypt(self, plain):
        aes = AES.new(self.key, AES.MODE_OFB, self.iv)
        return aes.encrypt(plain)
    def decrypt(self, cipher):
        aes = AES.new(self.key, AES.MODE_OFB, self.iv)
        return aes.decrypt(cipher)

key = os.urandom(16)
iv = os.urandom(16)

aes = AES_OFB(key, iv)

pt_0 = b"5HU5VhSHRrq0eJRW"
ct_0 = aes.encrypt(pt_0)

pt_1 = b"I_am_the_admin:)"
ct_1 = aes.encrypt(pt_1)

print(ct_0.hex())
# print("The FLAG is NeSE{" + ct_1.hex() + "}")
