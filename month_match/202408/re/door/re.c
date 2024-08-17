#include <stdio.h>
int ori[8] = {0x415f6231,0x745f3066,0x5f623174,0x5f736831,0x6654694e,0x675f6463,0x38306532,0x38313234};
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
