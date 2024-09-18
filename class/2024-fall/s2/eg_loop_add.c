#include <stdio.h>
int main()
{
    int sum = 0;
    for (int i = 1; i <= 10000; i++) {
        sum += i;
    }
    printf("1 + 2 + ... + 10000 = %d\n", sum);
    return 0;
}
