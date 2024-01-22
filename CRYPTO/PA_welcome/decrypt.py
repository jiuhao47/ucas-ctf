key = "welcome_to_the_crypto_world!"
ctxt_1 = open("./output.txt", "r")
ctxt_1.content = ctxt_1.read()


# chr() 用一个范围在 range（256）内的（就是0～255）整数作参数
# 返回一个对应的字符，当前整数对应的 ASCII 字符
# ord() 函数是 chr() 函数（对于8位的ASCII字符串）或 unichr() 函数（对于Unicode对象）的配对函数
# 它以一个字符（长度为1的字符串）作为参数，返回对应的 ASCII 数值，或者 Unicode 数值，
# 如果所给的 Unicode 字符超出了你的 Python 定义范围，则会引发一个 TypeError 的异常。
def decrypt(key, ct):
    pt = ""
    for i in range(len(ct)):
        pt += chr(
            (
                ((ord(ct[i]) - 0x20) + (0x7E - 0x20 + 1))
                + 0x20
                - (ord(key[i % len(key)]))
            )
            + 0x20
        )

    return pt


pt = decrypt(key, ctxt_1.content)
print(pt)

# 没找出哪里写错了，于是乎打表出奇迹，凑出了flag
