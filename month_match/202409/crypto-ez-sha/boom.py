from hashlib import sha256
from itertools import product

# 已知的secrets前30个字符
known_secrets = "2d94c7bd-37ac-4b3d-874b-aac9f1"

# 给出的哈希值
given_hash = 'e5b3a915d72dd0b4d90700a46614f5607204aac6dc1076c817e1a39b66c71a07'

# 所有可能的字符
chars = '0123456789abcdef'

# 尝试所有可能的剩余字符组合
for rest in product(chars, repeat=6):
    # 构造可能的secrets字符串
    secrets = (known_secrets + ''.join(rest)).encode()
    # 计算哈希值
    hash_value = sha256(secrets).hexdigest()
    # 如果哈希值匹配，打印出secrets和flag
    if hash_value == given_hash:
        print(f"Found secrets: {secrets}")
        print(f"Flag: flag{{{secrets.decode()}}}")
        break

# flag{2d94c7bd-37ac-4b3d-874b-aac9f1be97f5}
