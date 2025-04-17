# Time-up

## File Analysis

```shell
file times-up
```

times-up: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=578bcd6434fc9bd11298e7fef6e2902881cc0aa9, not stripped

## Reverse Analysis

```c
int main(void)
{
  init_randomness();
  printf("Challenge: ");
  generate_challenge();
  putchar(10);
  fflush(stdout);
  puts("Setting alarm...");
  fflush(stdout);
  ualarm(0x64780,0);
  printf("Solution? ");
  __isoc99_scanf(&DAT_00100e68,&guess);
  if (guess == result) {
    puts("Congrats! Here is the flag!");
    system("/bin/cat flag.txt");
  }
  else {
    puts("Nope!");
  }
  return 0;
}
```

It generate a random challenge and set an alarm for 0x64780 microseconds (0.4 seconds). The program then waits for user input and checks if the input matches the result of generated challenge. If it does, it prints the flag; otherwise, it prints "Nope!".

## Exploit

we need to get the challenge and calculate it

I use python function `eval` to calculate the challenge.

```python
#!/usr/bin/python
from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51008)
r.recvuntil(b"Challenge: ")
line1 = r.recvline(keepends=False)
expression = line1.decode("utf-8")
answer = eval(expression)
print(answer)
# to bytes
answer = str(answer).encode("utf-8")
r.sendline(answer)
r.interactive()
```



