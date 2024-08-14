#include <stdio.h>
#include <stdlib.h>

int main()
{
    // printf("%x", atoi("4189673334"));
    unsigned int i = atoi("4189673334");
    int j = 3 * i;
    /*
    while (i < 5)
    {
        j = j + 3;
        i = i + 1;
        printf("i=0x%x,j=0x%x\n", i, j);
    }
    */
    printf("%x", j);
    return 0;
}