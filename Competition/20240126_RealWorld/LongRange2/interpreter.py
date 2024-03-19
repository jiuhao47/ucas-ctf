import struct
import array

file = open("flash_dump", "rb")
info = file.read(20000000)
file_1 = open("output.txt", "w")
file_1.write(str(info))
