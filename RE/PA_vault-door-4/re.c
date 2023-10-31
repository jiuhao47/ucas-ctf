#include <stdio.h>
int main()
{
    int assci[24] = {
        106,
        85,
        53,
        116,
        95,
        52,
        95,
        98,
        0x55,
        0x6e,
        0x43,
        0x68,
        0x5f,
        0x30,
        0x66,
        0x5f,
        0142,
        0131,
        0164,
        063,
        0163,
        0137,
        070,
        0146,
    };
    for (int i = 0; i < 24; i++)
    {
        printf("%c", assci[i]);
    }
    return 0;
}
// 不难
