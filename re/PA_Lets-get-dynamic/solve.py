A_hex = [
    "0x364f08a25a57ba2a",
    "0x59e772982244bccb",
    "0xe7bdb8cf9f67cfa7",
    "0x3b635482ec0f7d53",
    "0x9baac4ce93a19129",
    "0x9fafdc131d6db828",
    "0x0000000000000061",
]
B_hex = [
    "0x563f52ce0f15cd77",
    "0x719435c3652ef38f",
    "0x8bec9fe9be05a4c9",
    "0x521c05fe8d590431",
    "0xdbf1c3a6dadcef7b",
    "0xc4fc8b585631f076",
    "0x000000000000003F",
]


def split_to_bytes(hex_list):
    byte_list = []
    for hex_str in hex_list:
        # Remove the '0x' prefix and split into pairs of two characters
        bytes_str = [f"0x{hex_str[i:i+2]}" for i in range(2, len(hex_str), 2)]
        # bytes_str.reverse()
        bytes_str.reverse()
        byte_list.extend(bytes_str)
    return byte_list


A_bytes = split_to_bytes(A_hex)
B_bytes = split_to_bytes(B_hex)

print("A_bytes:", A_bytes)
print("B_bytes:", B_bytes)

# Convert hex strings to integers
A_int = [int(x, 16) for x in A_bytes]
B_int = [int(x, 16) for x in B_bytes]
print(A_int)
print(B_int)

f = ""
for i in range(len(A_int)):
    c = (A_int[i] ^ B_int[i] ^ i) ^ 19
    f += chr(c)
print(f)
