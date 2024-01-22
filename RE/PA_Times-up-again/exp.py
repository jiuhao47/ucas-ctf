#!/usr/bin/python
from ctypes import *
from pwn import *


def cal(a, b, c):
    if c == 43:
        temp = a + b
    elif c == 45:
        temp = a - b
    elif c == 42:
        temp = a * b
    return temp


solver = CDLL("./solve.so")
context.arch = "amd64"
r = remote("124.16.75.117", 51001)
r.recvuntil(b"Challenge: ")
line1 = r.recvline(keepends=False)
print(line1)

mid1 = cal(
    solver.solve(line1, 0, 0), solver.solve(line1, 0, 1), solver.solve(line1, 1, 0)
)
mid2 = cal(
    solver.solve(line1, 0, 2), solver.solve(line1, 0, 3), solver.solve(line1, 1, 2)
)
mid3 = cal(mid1, mid2, solver.solve(line1, 1, 1))
mid4 = cal(
    solver.solve(line1, 0, 4), solver.solve(line1, 0, 5), solver.solve(line1, 1, 4)
)
mid5 = cal(
    solver.solve(line1, 0, 6), solver.solve(line1, 0, 7), solver.solve(line1, 1, 6)
)
mid6 = cal(mid4, mid5, solver.solve(line1, 1, 5))
mid7 = cal(mid3, mid6, solver.solve(line1, 1, 3))
mid1 = cal(
    solver.solve(line1, 0, 8), solver.solve(line1, 0, 9), solver.solve(line1, 1, 8)
)
mid2 = cal(
    solver.solve(line1, 0, 10), solver.solve(line1, 0, 11), solver.solve(line1, 1, 10)
)
mid3 = cal(mid1, mid2, solver.solve(line1, 1, 9))
mid4 = cal(
    solver.solve(line1, 0, 12), solver.solve(line1, 0, 13), solver.solve(line1, 1, 12)
)
mid5 = cal(
    solver.solve(line1, 0, 14), solver.solve(line1, 0, 15), solver.solve(line1, 1, 14)
)
mid6 = cal(mid4, mid5, solver.solve(line1, 1, 13))
mid8 = cal(mid3, mid6, solver.solve(line1, 1, 11))
answer = cal(mid7, mid8, solver.solve(line1, 1, 7))
print(answer)
r.sendline(str(answer))
r.interactive()
