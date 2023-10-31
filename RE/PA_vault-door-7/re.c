#include <stdio.h>
int ori[8] = {1096770097, 1952395366, 1600270708, 1601398833, 1716808014, 1734304867, 942695730, 942748212};
int main()

{
    for (int i = 0; i < 8; i++)
    {
        printf("%c", (ori[i] & 0xff000000) >> 24);
        printf("%c", (ori[i] & 0x00ff0000) >> 16);
        printf("%c", (ori[i] & 0x0000ff00) >> 8);
        printf("%c", (ori[i] & 0x000000ff));
    }
    return 0;
}
// 不难