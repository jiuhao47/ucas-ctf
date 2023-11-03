#include <stdio.h>
int check(int x, int y);
int main()
{
    int x, y, z;
    x = 1;
    y = 1;
    z = 0;
    while (y <= 20) // y=130040开始，t豁口
    {
        x = 1;
        while (x <= 31)
        {
            z = check(x, y);
            if (x == 13 || x == 17)
            {
                if (z != 0)
                {
                    // printf("%d\n", y);
                }
            }

            // printf("on\n");
            if (z != 0)
            {
                printf("%d:%c,%d\n", x, x - 1 + 'A', y);
            }

            ++x;
        }
        // int k;
        // k = ((0x0000555555556040 + y * 8) >> (x & 0b00111111)) & 0b00000001;
        // if (k == 0)
        //{
        //   printf("%d\n", y);
        //}

        ++y;
    }

    return 0;
}
int check(int x, int y)
{
    return ((0xff + y * 8) >> (x & 0b00111111)) & 0b00000001;
}