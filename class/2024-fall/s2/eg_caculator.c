#include <stdio.h>
int main()
{
    int a, b;
    printf("请输入两个整数：");
    scanf("%d %d", &a, &b);
    char op;
    printf("请输入运算符：");
    scanf(" %c", &op);
    if (op == '+') {
        printf("%d + %d = %d\n", a, b, a + b);
    } else if (op == '-') {
        printf("%d - %d = %d\n", a, b, a - b);
    } else if (op == '*') {
        printf("%d * %d = %d\n", a, b, a * b);
    } else {
        printf("不支持的运算符\n");
    }
    return 0;
}
