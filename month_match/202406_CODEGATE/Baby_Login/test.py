import hashlib


def validate_hash(hash_value):
    shifted = hash_value >> 24
    shifted = shifted << 24
    return shifted == hash_value


# 这是给定的随机字符串
random_string = "GI7YU7GIK1H78LHX"
print("PoW > " + random_string)

i = 0
while True:
    answer = str(i)
    concatenated = random_string + answer
    hash_object = hashlib.sha256(concatenated.encode())
    hash_value = int(hash_object.hexdigest(), 16)

    if validate_hash(hash_value):
        print("Found valid PoW:", answer)
        break

    i += 1
