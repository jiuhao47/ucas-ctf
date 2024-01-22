#include <stdio.h>
int main()
{
    char mystr[] = "NeSE_a3112";
    int i = 10;
    int y = 1;
    int x = 0x246;
    while (y < i - 1)
    {
        x = x + (mystr[y + 1]) - (mystr[y - 1]);
        y++;
    }
    printf("0x%x", x);
}