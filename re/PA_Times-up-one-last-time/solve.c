#include <stdio.h>
#include <ctype.h>
#include <string.h>
long long int cal(long long int a, long long int b, char operand);
long long int solve(char s[], int type, int index)
{
    long long int answer = 0;

    long long int op[17];
    char operand[16];
    sscanf(s, "(((((%lld) %c (%lld)) %c ((%lld) %c (%lld))) %c (((%lld) %c (%lld)) %c ((%lld) %c (%lld)))) %c ((((%lld) %c (%lld)) %c ((%lld) %c (%lld))) %c (((%lld) %c ((%lld) %c (%lld))) %c ((%lld) %c (%lld)))))", &op[0], &operand[0], &op[1], &operand[1], &op[2], &operand[2], &op[3], &operand[3], &op[4], &operand[4], &op[5], &operand[5], &op[6], &operand[6], &op[7], &operand[7], &op[8], &operand[8], &op[9], &operand[9], &op[10], &operand[10], &op[11], &operand[11], &op[12], &operand[12], &op[13], &operand[13], &op[14], &operand[14], &op[15], &operand[15], &op[16]);
    // printf("%s\n", s);
    if (type == 0)
    {
        answer = op[index];
    }
    else
    {
        answer = operand[index];
    }
    /*
    long long int mid1 = 0;
    mid1 = cal(op[0], op[1], operand[0]);
    long long int mid2 = 0;
    mid2 = cal(op[2], op[3], operand[2]);
    long long int mid3 = 0;
    mid3 = cal(mid1, mid2, operand[1]);
    long long int mid4 = 0;
    mid4 = cal(op[4], op[5], operand[4]);
    long long int mid5 = 0;
    mid5 = cal(op[6], op[7], operand[6]);
    long long int mid6 = 0;
    mid6 = cal(mid4, mid5, operand[5]);
    long long int mid7 = 0;
    mid6 = cal(mid3, mid6, operand[3]);

    mid1 = 0;
    mid1 = cal(op[8], op[9], operand[8]);
    mid2 = 0;
    mid2 = cal(op[10], op[11], operand[10]);
    mid3 = 0;
    mid3 = cal(mid1, mid2, operand[9]);
    mid4 = 0;
    mid4 = cal(op[12], op[13], operand[12]);
    mid5 = 0;
    mid5 = cal(op[14], op[15], operand[14]);
    mid6 = 0;
    mid6 = cal(mid4, mid5, operand[13]);
    long long int mid8 = 0;
    mid8 = cal(mid3, mid6, operand[11]);

    answer = cal(mid7, mid8, operand[7]);
    */

    return answer;
}

long long int cal(long long int a, long long int b, char operand)
{
    long long int temp;
    switch (operand)
    {
    case '+':
        temp = a + b;
        break;
    case '-':
        temp = a - b;
        break;
    case '*':
        temp = a * b;
        break;
    case '/':
        temp = a / b;
        break;
    }
    return temp;
}
