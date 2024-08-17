#!/usr/bin/env python3

import subprocess
import cv2
import hashlib
import numpy as np
import matplotlib.pyplot as plt

"""
加密函数
img:原始图像路径
key:密钥列表，大小为9(1、2为PWLCM初始条件和参数；3、4、5、6为Chen系统初值，7、8、9为Lorenz系统初值)
return:返回加密后的图像
"""


def encrypt(img, key):
    # 读取图片
    # opencv的颜色通道顺序为[B,G,R]，而matplotlib颜色通道顺序为[R,G,B],所以需要调换一下通道位置
    im = cv2.imread(img)[:, :, (2, 1, 0)]
    # 获取图像宽高和通道数
    [w, h, dim] = im.shape

    # 生成初始条件
    a0 = key[0]
    p0 = key[1]
    u0 = key[2]
    v0 = key[3]
    w0 = key[4]
    x0 = key[5]
    y0 = key[6]
    z0 = key[7]
    q0 = key[8]

    # 两次置乱操作
    # 图像扁平化为一维,flatten in row-major
    pixels = im.flatten(order="C")

    # 第一次置乱
    # PWLCM迭代3*w*h次，得到迭代序列ai
    ai = []
    for i in range(3 * w * h):
        if 0 <= a0 < p0:
            a0 = a0 / p0
        elif a0 < 0.5:
            a0 = (a0 - p0) * (0.5 - p0)
        else:
            a0 = 1 - a0
        ai.append(a0)
    # 打包
    dic = list(zip(ai, pixels))
    # 根据ai排序
    dic.sort(key=lambda x: x[0])
    # 得到排序后的像素列表
    pixels = list(list(zip(*dic))[1])
    # 分成R、G、B三个通道
    R = pixels[: w * h]
    G = pixels[w * h : 2 * w * h]
    B = pixels[2 * w * h :]

    # 第二次置乱
    # Lorenz生成三个序列Y,Z,Q
    t = 100
    f = 10
    r = 28
    g = 8 / 3
    # 调用Lorenz模型函数
    Y, Z, Q = Lorenz(y0, z0, q0, f, r, g, t + w * h)
    # 丢弃序列前t个值
    Y = Y[t:]
    Z = Z[t:]
    Q = Q[t:]
    # 分别在R、G、B三个通道进行排序
    Y_R = list(zip(Y, R))
    # 根据序列Y排序
    Y_R.sort(key=lambda x: x[0])
    # 得到排序后的像素列表
    R = list(list(zip(*Y_R))[1])
    Z_G = list(zip(Z, G))
    # 根据序列Z排序
    Z_G.sort(key=lambda x: x[0])
    # 得到排序后的像素列表
    G = list(list(zip(*Z_G))[1])
    Q_B = list(zip(Q, B))
    # 根据序列Q排序
    Q_B.sort(key=lambda x: x[0])
    # 得到排序后的像素列表
    B = list(list(zip(*Q_B))[1])

    # 得到重新排列后的R、G、B颜色分量
    # DNA编码
    # Hyper Chaos Chen系统控制参数
    a = 36
    b = 3
    c = 28
    d = 16
    k = 0.2
    t = 100
    U, V, W, X = Chen(u0, v0, w0, x0, a, b, c, d, k, t + 3 * w * h)
    U = U[t:]
    V = V[t:]
    W = W[t:]
    X = X[t:]
    for i in range(3 * w * h):
        rule = "ACGT"
        if int(U[i] % 1 / 0.05) in [0, 4, 8, 10, 19]:
            # 采用编码规则AGCT
            rule = "AGCT"
        elif int(U[i] % 1 / 0.05) in [1, 6, 12, 14, 17]:
            # 编码规则ACGT
            rule = "ACGT"
        elif int(U[i] % 1 / 0.05) in [2, 7, 11, 13, 16]:
            rule = "GATC"
        elif int(U[i] % 1 / 0.05) in [3, 5, 9, 15, 18]:
            rule = "CATG"
        if i / (w * h) < 1:
            R[i] = DNA_Encode(R[i], rule)
        elif i / (w * h) < 2:
            G[i - w * h] = DNA_Encode(G[i - w * h], rule)
        else:
            B[i - 2 * w * h] = DNA_Encode(B[i - 2 * w * h], rule)

    start = []
    times = []
    for i in V:
        start.append(int(i * pow(10, 12)) % 8)
    for i in W:
        times.append(int(i * pow(10, 12)) % 8)

    startR = start[: w * h]
    startG = start[w * h : 2 * w * h]
    startB = start[2 * w * h :]

    timesR = times[: w * h]
    timesG = times[w * h : 2 * w * h]
    timesB = times[2 * w * h :]
    # 八种DNA编码规则
    rules = ["ACGT", "CATG", "GTAC", "TCGA", "CTAG", "AGCT", "TGCA", "GATC"]
    for i in range(w * h):
        # 起始规则位置
        s = startR[i]
        for j in range(timesR[i]):
            R[i] = DNA_XOR(R[i], rules[s])
            s = (s + 1) % 8

    for i in range(w * h):
        # 起始规则位置
        s = startG[i]
        for j in range(timesG[i]):
            G[i] = DNA_XOR(G[i], rules[s])
            s = (s + 1) % 8

    for i in range(w * h):
        # 起始规则位置
        s = startB[i]
        for j in range(timesB[i]):
            B[i] = DNA_XOR(B[i], rules[s])
            s = (s + 1) % 8

    # DNA解码
    for i in range(3 * w * h):
        rule = "ACGT"
        if int(X[i] % 1 / 0.05) in [0, 4, 8, 10, 19]:
            # 采用解码规则GTAC
            rule = "GTAC"
        elif int(X[i] % 1 / 0.05) in [1, 6, 12, 14, 17]:
            # 解码规则TGCA
            rule = "TGCA"
        elif int(X[i] % 1 / 0.05) in [2, 7, 11, 13, 16]:
            rule = "CTAG"
        elif int(X[i] % 1 / 0.05) in [3, 5, 9, 15, 18]:
            rule = "TCGA"
        if i / (w * h) < 1:
            R[i] = DNA_Decode(R[i], rule)
        elif i / (w * h) < 2:
            G[i - w * h] = DNA_Decode(G[i - w * h], rule)
        else:
            B[i - 2 * w * h] = DNA_Decode(B[i - 2 * w * h], rule)

    # 合并R、G、B三个通道得到加密彩色图像
    encrypt_img = np.array((R + G + B)).reshape((512, 512, 3), order="C")
    return encrypt_img


"""
功能：加密图像解密，加密过程的逆
参数：
输入加密图像路径和密钥参数
返回：
返回解密后的图像(ndarray)
"""


def decrypt(img, key):
    # 生成初始条件
    a0 = key[0]
    p0 = key[1]
    u0 = key[2]
    v0 = key[3]
    w0 = key[4]
    x0 = key[5]
    y0 = key[6]
    z0 = key[7]
    q0 = key[8]

    # 读取密文图像
    # im=cv2.imread(img)[:,:,(2,1,0)]
    im = cv2.imread(img)
    # 获取图像高宽和通道数
    [h, w, dim] = im.shape
    pixels = im.flatten(order="C")
    # 分成R、G、B三个通道
    R = list(pixels[: w * h])
    G = list(pixels[w * h : 2 * w * h])
    B = list(pixels[2 * w * h :])
    # Hyper Chaos Chen系统控制参数
    a = 36
    b = 3
    c = 28
    d = 16
    k = 0.2
    t = 100
    U, V, W, X = Chen(u0, v0, w0, x0, a, b, c, d, k, t + 3 * w * h)
    U = U[t:]
    V = V[t:]
    W = W[t:]
    X = X[t:]

    for i in range(3 * w * h):
        rule = "ACGT"
        if int(X[i] % 1 / 0.05) in [0, 4, 8, 10, 19]:
            # 采用解码规则GTAC进行逆编码
            rule = "GTAC"
        elif int(X[i] % 1 / 0.05) in [1, 6, 12, 14, 17]:
            # 解码规则TGCA
            rule = "TGCA"
        elif int(X[i] % 1 / 0.05) in [2, 7, 11, 13, 16]:
            rule = "CTAG"
        elif int(X[i] % 1 / 0.05) in [3, 5, 9, 15, 18]:
            rule = "TCGA"

        if i / (w * h) < 1:
            R[i] = DNA_Encode(R[i], rule)
        elif i / (w * h) < 2:
            G[i - w * h] = DNA_Encode(G[i - w * h], rule)
        else:
            B[i - 2 * w * h] = DNA_Encode(B[i - 2 * w * h], rule)

    # 逆扩散
    start = []
    times = []
    for i in V:
        start.append(int(i * pow(10, 12)) % 8)
    for i in W:
        times.append(int(i * pow(10, 12)) % 8)
    # 这里要你自已补全
    startR = start[: w * h]
    startG = start[w * h : 2 * w * h]
    startB = start[2 * w * h :]
    timesR = times[: w * h]
    timesG = times[w * h : 2 * w * h]
    timesB = times[2 * w * h :]
    # 八种DNA编码规则
    rules = ["ACGT", "CATG", "GTAC", "TCGA", "CTAG", "AGCT", "TGCA", "GATC"]
    for i in range(w * h):
        s = (startR[i] + timesR[i] - 1) % 8
        for j in range(timesR[i]):
            R[i] = DNA_XOR(R[i], rules[s])
            s = (s - 1) % 8
    for i in range(w * h):
        # 起始规则位置
        s = (startG[i] + timesG[i] - 1) % 8
        for j in range(timesG[i]):
            G[i] = DNA_XOR(G[i], rules[s])
            s = (s - 1) % 8
    for i in range(w * h):
        # 起始规则位置
        s = (startB[i] + timesB[i] - 1) % 8
        for j in range(timesB[i]):
            B[i] = DNA_XOR(B[i], rules[s])
            s = (s - 1) % 8

    # 逆编码
    for i in range(3 * w * h):
        rule = "ACGT"
        if int(U[i] % 1 / 0.05) in [0, 4, 8, 10, 19]:
            # 采用编码规则AGCT
            rule = "AGCT"
        elif int(U[i] % 1 / 0.05) in [1, 6, 12, 14, 17]:
            # 编码规则ACGT
            rule = "ACGT"
        elif int(U[i] % 1 / 0.05) in [2, 7, 11, 13, 16]:
            rule = "GATC"
        elif int(U[i] % 1 / 0.05) in [3, 5, 9, 15, 18]:
            rule = "CATG"
        if i / (w * h) < 1:
            R[i] = DNA_Decode(R[i], rule)
        elif i / (w * h) < 2:
            G[i - w * h] = DNA_Decode(G[i - w * h], rule)
        else:
            B[i - 2 * w * h] = DNA_Decode(B[i - 2 * w * h], rule)

    # 逆第二次置乱
    # Lorenz生成三个序列Y,Z,Q
    t = 100
    f = 10
    r = 28
    g = 8 / 3
    # 调用Lorenz模型函数
    Y, Z, Q = Lorenz(y0, z0, q0, f, r, g, t + w * h)
    # 丢弃序列前t个值
    Y = Y[t:]
    Z = Z[t:]
    Q = Q[t:]

    # 分别在R、G、B三个通道进行排序
    seq = range(w * h)
    Y_seq = list(zip(Y, seq))
    # 根据序列Y得到R通道真实的序列
    Y_seq.sort(key=lambda x: x[0])
    # 得到真实序列，Y元素为位置索引
    Y = list(list(zip(*Y_seq))[1])

    Z_seq = list(zip(Z, seq))
    Z_seq.sort(key=lambda x: x[0])
    Z = list(list(zip(*Z_seq))[1])

    Q_seq = list(zip(Q, seq))
    Q_seq.sort(key=lambda x: x[0])
    Q = list(list(zip(*Q_seq))[1])

    Y_R = list(zip(Y, R))
    Y_R.sort(key=lambda x: x[0])
    R = list(list(zip(*Y_R))[1])

    Z_G = list(zip(Z, G))
    Z_G.sort(key=lambda x: x[0])
    G = list(list(zip(*Z_G))[1])

    Q_B = list(zip(Q, B))
    Q_B.sort(key=lambda x: x[0])
    B = list(list(zip(*Q_B))[1])
    pixels = R + G + B
    # 逆第一次置乱
    # PWLCM迭代3*w*h次，得到迭代序列ai
    ai = []
    for i in range(3 * w * h):
        if 0 <= a0 < p0:
            a0 = a0 / p0
        elif a0 < 0.5:
            a0 = (a0 - p0) * (0.5 - p0)
        else:
            a0 = 1 - a0
        ai.append(a0)
    seq = range(3 * w * h)
    ai_seq = list(zip(ai, seq))
    # 根据序列ai得到真实的序列
    ai_seq.sort(key=lambda x: x[0])
    # 得到真实序列，ai元素为位置索引
    ai = list(list(zip(*ai_seq))[1])
    # 打包
    dic = list(zip(ai, pixels))
    # 根据ai排序
    dic.sort(key=lambda x: x[0])
    # 得到排序后的像素列表
    pixels = list(list(zip(*dic))[1])
    decrypt_img = np.array(pixels).reshape((512, 512, 3), order="C")
    return decrypt_img


"""
Lorenz吸引子生成函数
参数为三个初始坐标，三个初始参数,迭代次数
返回三个一维list
"""


def Lorenz(x0, y0, z0, p, q, r, T):
    # 微分迭代步长
    h = 0.01
    x = []
    y = []
    z = []
    for t in range(T):
        xt = x0 + h * p * (y0 - x0)
        yt = y0 + h * (q * x0 - y0 - x0 * z0)
        zt = z0 + h * (x0 * y0 - r * z0)
        # x0、y0、z0统一更新
        x0, y0, z0 = xt, yt, zt
        x.append(x0)
        y.append(y0)
        z.append(z0)
    return x, y, z


"""
Chen吸引子生成函数
参数为四个初始坐标，五个初始参数,迭代次数
返回四个一维数组(坐标)
"""


def Chen(u0, v0, w0, x0, a, b, c, d, k, T):
    h = 0.001
    u = []
    v = []
    w = []
    x = []
    for t in range(T):
        ut = u0 + h * (a * (v0 - u0))
        vt = v0 + h * (-u0 * w0 + d * u0 + c * u0 - x0)
        wt = w0 + h * (u0 * v0 - b * w0)
        xt = u0 + k
        # u0、v0、w0,x0统一更新
        u0, v0, w0, x0 = ut, vt, wt, xt
        u.append(u0)
        v.append(v0)
        w.append(w0)
        x.append(x0)
    return u, v, w, x


# 根据原始图像使用SHA256生成初始条件
def Generate_Key(img, key):
    im = cv2.imread(img)[:, :, (2, 1, 0)]
    # 获取图像高宽和通道数
    [h, w, dim] = im.shape
    with open(img, "rb") as f:
        bytes = f.read()
        img_hash = hashlib.sha256(bytes).hexdigest()
    m = []
    for i in range(8):
        m.append(int(img_hash[i * 7 : i * 7 + 7], 16) / 2**34)
    d = int(img_hash[-8:], 16) / 2**38
    ck = 0
    for i in range(len(key)):
        ck += key[i]
    # 生成初始条件
    for i in range(8):
        key[i] = (key[i] + m[i] + ck) % 1
    key[8] = (key[8] + d + ck) % 1
    return key


# 将像素值按照规则rule编码成DNA碱基返回
def DNA_Encode(pixel, rule):
    base = ""
    # 将整数像素值转成8bits二进制
    bits = bin(pixel)[2:].zfill(8)
    for k in range(4):
        b = bits[k * 2 : 2 * k + 2]
        if b == "00":
            base += rule[0]
        elif b == "01":
            base += rule[1]
        elif b == "10":
            base += rule[2]
        else:
            base += rule[3]
    return base


# 将4个DNA碱基组成的字符串按rule解码成像素值返回
def DNA_Decode(base, rule):
    pixel = ""
    for k in base:
        if k == rule[0]:
            pixel += "00"
        elif k == rule[1]:
            pixel += "01"
        elif k == rule[2]:
            pixel += "10"
        else:
            pixel += "11"
    return int(pixel, 2)


def DNA_XOR(base1, base2):
    # 转成整数进行异或
    pixel = DNA_Decode(base1, "AGCT") ^ DNA_Decode(base2, "AGCT")
    return DNA_Encode(pixel, "AGCT")


def main():
    # 原始图像路径
    img_path = "./image512.png"

    # 从文件读取加密密钥参数列表
    key_file_path = "./key"
    # 读取 key 文件内容
    with open(key_file_path, "r") as file:
        key = [float(x) for x in file.readline().strip()[1:-1].split(",")]

    new_key = Generate_Key(img_path, key)
    # 原始图像
    img = cv2.imread(img_path)[:, :, (2, 1, 0)]
    # 加密后的图像
    img_encrypt = encrypt(img_path, new_key)
    cv2.imwrite("./image_encrypt.png", img_encrypt)
    decrypt_path = "./image_processed.png"
    # 正确密钥解密图像
    img_decrypt = decrypt(decrypt_path, new_key)
    # 错误密钥解密图像
    wrong_key = list(new_key)
    wrong_key[8] += pow(10, -10)
    wrong_decrypt = decrypt(decrypt_path, wrong_key)

    # 结果展示
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 中文乱码
    # 子图1，原始图像
    plt.subplot(221)
    # imshow()对图像进行处理，画出图像，show()进行图像显示
    plt.imshow(img)
    plt.title("原始图像")
    # 不显示坐标轴
    plt.axis("off")

    # 子图2，加密后图像
    plt.subplot(222)
    plt.imshow(img_encrypt)
    plt.title("加密图像\nq0={}".format(new_key[8]))
    plt.axis("off")

    # 子图3，错误密钥解密结果
    plt.subplot(223)
    plt.imshow(wrong_decrypt)
    plt.title("解密图像\nq0={}".format(wrong_key[8]))
    plt.axis("off")

    # 子图4，正确密钥解密结果
    plt.subplot(224)
    plt.imshow(img_decrypt)
    plt.title("解密图像\nq0={}".format(new_key[8]))
    plt.axis("off")

    # #设置子图默认的间距
    plt.tight_layout()
    # 显示图像
    plt.show()


if __name__ == "__main__":
    main()
