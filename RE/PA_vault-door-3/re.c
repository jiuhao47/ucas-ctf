#include <stdio.h>
int main()
{
    char pass[] = "jU5t_a_sna_3lpm18g947_u_4_m9r54f";
    char s[32];
    int i;
    for (i = 0; i < 8; i++)
    {
        s[i] = pass[i];
    }
    for (; i < 16; i++)
    {
        s[i] = pass[23 - i];
    }
    for (; i < 32; i += 2)
    {
        s[i] = pass[46 - i];
    }
    for (i = 31; i >= 17; i -= 2)
    {
        s[i] = pass[i];
    }
    printf("%s", s);
    return 0;
}
// 不难，直接过