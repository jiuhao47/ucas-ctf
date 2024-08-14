#include <stdio.h>
int a = 0x20240417;
int b = 91;
int c = 26;
int mid = 0;
int main()
{
    mid = b % c;
    while (mid != 0)
    {
        a = ((a * 2 + 5) / 16 - 11) ^ 0x1004F02C;
        mid = b % c;
        c = c + 13;
    }
    printf("0x%x", a);
    return 0;
}