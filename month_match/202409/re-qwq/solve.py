import struct

def shld(a1, a2):
    return (a1 << 1 | a2 >> 31) & 0xFFFFFFFF

# a1的最低位改为a2的最高位


def shl(a1):
    return a1 << 1 & 0xFFFFFFFF

# a1左移1位

def shr(a1):
    return a1 >> 1 & 0xFFFFFFFF

# a1右移1位

def en(buf):
    for i in range(0, 10, 2):
        ta = buf[i]
        tb = buf[i + 1]
        for k in range(64):
            if tb & 0x80000000 == 0x80000000:
                tb = shld(tb, ta)
                ta = shl(ta)
                ta = (0x54AA4A9 ^ ta) & 0xFFFFFFFF
            else:
                tb = shld(tb, ta)
                ta = shl(ta)
        else:
            buf[i] = ta
            buf[i + 1] = tb

def de(buf):
    for i in range(0, 10, 2):
        ta = buf[i]
        tb = buf[i + 1]
        for k in range(64):
            if ta & 1 == 1:
                ta = (0x54AA4A9 ^ ta) & 0xFFFFFFFF
                ta = shr(ta) | ((tb & 0x00000001)<<31)
                tb = shr(tb) | 0x80000000
            else:
                ta = shr(ta) | ((tb & 0x00000001) << 31)
                tb = shr(tb)
        buf[i] = ta
        buf[i + 1] = tb

def int_to_chars(i):
    # 将整数拆分为4个字节
    bytes1 = struct.pack('>I', i)
    print(bytes1)
    # 翻转每组的顺序
    reversed_bytes = bytes1[::-1]
    print(reversed_bytes)
    # 将每个字节转换为字符
    chars = [chr(b) for b in reversed_bytes]
    # 将字符拼接成字符串
    return ''.join(chars)


if __name__ == "__main__":
    res = [
        1314885045,
        52669423,
        3603395589,
        2403896625,
        2646202166,
        1248852717,
        3397747772,
        555389864,
        4216202737,
        2381736511,
    ]
    de(res)
    print(res)
    flag = ''.join([int_to_chars(i) for i in res])

    print(flag)


# flag{96e79218965eb72c92a549dd5a33011211}
