#!/usr/bin/env python3

# from secret import flag


def encrypt(key, pt):
    ct = ""
    for i in range(len(pt)):
        ct += chr(
            (
                ((ord(pt[i]) - 0x20) + (ord(key[i % len(key)]) - 0x20))
                % (0x7E - 0x20 + 1)
            )
            + 0x20
        )
    return ct


key = "welcome_to_the_crypto_world!"
# ct = encrypt(key, flag)

# print(ct)
