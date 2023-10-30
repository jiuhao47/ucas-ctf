#include <stdio.h>
int main()
{
    int i = 0;
    char flag_fake[] = "w1{1wq84fb<1>49";
    char c = '\0';
    while (i < 15)
    {
        if ((i & 1) == 0)
        {
            flag_fake[i] = flag_fake[i] - '\x05';
        }
        else
        {
            flag_fake[i] = flag_fake[i] + 2;
        }

        i++;
    }
    printf("%s", flag_fake);

    return 0;
}

// Ghidra 逆向，不难
// 看反汇编找找逻辑就行