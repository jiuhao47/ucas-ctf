flag = ""
flag1 = "乥卅筊畳瑟呲㑮獆ひ洴慴ㅯ湽"
for i in range(len(flag1)):
    # c = chr((ord(flag[i]) << 8) + ord(flag[i + 1]))
    flag = flag + chr(ord(flag1[i]) >> 8)
    flag = flag + chr(ord(flag1[i]) & 0xFF)
print(flag)
