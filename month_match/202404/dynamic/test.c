#include <stdio.h>
int f0(int c)
{
    return (((c * 37) % 129 << 3 ^ 165) + 31) % 257;
}
int array[23] = {0xcb, 0x71, 0x10, 0xb2, 0xa3, 0x4c, 0x10, 0x79, 0x82, 0x9a, 0xdb, 0x92, 0x33, 0x5b, 0xcb, 0xb2, 0xbc, 0xe3, 0x4a, 0x2b, 0x44, 0xf1};
int main()
{
    int temp;
    for (int i = 0; i < 22; i++)
    {
        for (int c = 32; c < 128; c++)
        {
            temp = f0(c);
            if (array[i] == temp)
            {
                printf("i=%d,c=%c(%d)\n", i, c, c);
                putchar(49);
            }
            else
            {
                // putchar(48);
            }
        }
    }
    putchar(50);
    return 0;
}

// lag{wasdytrxcfg123qp} S
