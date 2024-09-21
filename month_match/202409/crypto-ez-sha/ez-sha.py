from hashlib import sha256
from secret import flag, secrets

assert flag == b"flag{" + secrets + b"}"
assert secrets[:30] == b"2d94c7bd-37ac-4b3d-874b-aac9f1" and len(secrets) == 36
hash_value = sha256(secrets).hexdigest()
print(f"{hash_value = }")

#hash_value = 'e5b3a915d72dd0b4d90700a46614f5607204aac6dc1076c817e1a39b66c71a07'
