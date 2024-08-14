#include <stdio.h>
#include <ctype.h>
#include <string.h>
int solve(char s[])
{
    int answer = 0;

    int op[16];
    char operand[15];
    sscanf(s, "(((((%d) %c (%d)) %c ((%d) %c (%d))) %c (((%d) %c (%d)) %c ((%d) %c (%d)))) %c ((((%d) %c (%d)) %c ((%d) %c (%d))) %c (((%d) %c (%d)) %c ((%d) %c (%d)))))", &op[0], &operand[0], &op[1], &operand[1], &op[2], &operand[2], &op[3], &operand[3], &op[4], &operand[4], &op[5], &operand[5], &op[6], &operand[6], &op[7], &operand[7], &op[8], &operand[8], &op[9], &operand[9], &op[10], &operand[10], &op[11], &operand[11], &op[12], &operand[12], &op[13], &operand[13], &op[14], &operand[14], &op[15]);
    printf("%s\n", s);
    answer = answer + op[0];
    int mid1 = 0;
    mid1 = (operand[0] == '+') ? op[0] + op[1] : op[0] - op[1];
    int mid2 = 0;
    mid2 = (operand[2] == '+') ? op[2] + op[3] : op[2] - op[3];
    int mid3 = 0;
    mid3 = (operand[1] == '+') ? mid1 + mid2 : mid1 - mid2;
    int mid4 = 0;
    mid4 = (operand[4] == '+') ? op[4] + op[5] : op[4] - op[5];
    int mid5 = 0;
    mid5 = (operand[6] == '+') ? op[6] + op[7] : op[6] - op[7];
    int mid6 = 0;
    mid6 = (operand[5] == '+') ? mid4 + mid5 : mid4 - mid5;
    int mid7 = 0;
    mid7 = (operand[3] == '+') ? mid3 + mid6 : mid3 - mid6;

    mid1 = 0;
    mid1 = (operand[8] == '+') ? op[8] + op[9] : op[8] - op[9];
    mid2 = 0;
    mid2 = (operand[10] == '+') ? op[10] + op[11] : op[10] - op[11];
    mid3 = 0;
    mid3 = (operand[9] == '+') ? mid1 + mid2 : mid1 - mid2;
    mid4 = 0;
    mid4 = (operand[12] == '+') ? op[12] + op[13] : op[12] - op[13];
    mid5 = 0;
    mid5 = (operand[14] == '+') ? op[14] + op[15] : op[14] - op[15];
    mid6 = 0;
    mid6 = (operand[13] == '+') ? mid4 + mid5 : mid4 - mid5;
    int mid8 = 0;
    mid8 = (operand[11] == '+') ? mid3 + mid6 : mid3 - mid6;

    answer = (operand[7] == '+') ? mid7 + mid8 : mid7 - mid8;
    return answer;
}