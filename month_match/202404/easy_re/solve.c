#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    char num1[4] = "flag";
    char content[100];
    char array[40];
    int flag = 0x64636261;
    int mid1;
    char mid2;
    int mid3;
    int count = 0;
    int j = 0;
    while (1)
    {
        mid1 = 4;
        if (mid1 <= j)
        {
            break;
        }
        mid2 = num1[j];
        for (int i = 7; -1 < i; i = i - 1)
        {
            if ((mid2 >> (i & 0x1f) & 1) == 0)
            {
                array[(7 - i) + j * 8] = '0';
            }
            else
            {
                array[(7 - i) + j * 8] = '1';
            }
        }
        j = j + 1;
    }
    for (j = 0; j < 0x10; j = j + 1)
    {
        count = 0;
        for (int i = 0; i < 2; i = i + 1)
        {
            if (j == i)
            {
                mid3 = array[j + i * 0x10] - 0x30;
            }
            else
            {
                mid3 = (j + i) * (array[j + i * 0x10] - 0x30);
            }
            count = count + mid3;
        }
        content[j] = count + (count / 0x1a) * (-0x1a) + 'a';
    }
    printf("flag{");
    for (int i = 0; i < 100; i++)
    {
        printf("%c", content[i]);
    }
    printf("}");
    return 0;
}