#include <stdio.h>
#include <stdlib.h>
int main()
{
    unsigned int i = atoi("2541039191");
    int j = 0;
    int k = 0;
    int temp;
    while (i != 0)
    {
        temp = i & 0x1;
        i = i >> 1;
        if (temp != 0)
        {
            k = j;
            j = k + 3;
        }
        printf("j=%x\n", j);
    }
    printf("j=%x\n", j);
}
