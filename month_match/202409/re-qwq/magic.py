MAGIC_NUMBER = (3425).to_bytes(2, 'little') + b'\r\n'
_RAW_MAGIC_NUMBER = int.from_bytes(MAGIC_NUMBER, 'little')  # For import.c
HEX_MAGIC_NUMBER = hex(_RAW_MAGIC_NUMBER)
print(HEX_MAGIC_NUMBER)

