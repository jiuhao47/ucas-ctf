#include <stdio.h>
#include <string.h>
#include <stdlib.h>
char switchBits(char c, int p1, int p2);
char re_scramble(char a);
char ct[32] = {0xF4, 0xC0, 0x97, 0xF0, 0x77,
               0x97, 0xC0, 0xE4, 0xF0, 0x77,
               0xA4, 0xD0, 0xC5, 0x77, 0xF4,
               0x86, 0xD0, 0xA5, 0x45, 0x96,
               0x27, 0xB5, 0x77, 0xE0, 0x95,
               0xF1, 0xE1, 0xE0, 0xA4, 0xC0,
               0x94, 0xA4};
char re[100];
int main()
{
    // printf("begin\n");
    for (int b = 0; b < 32; b++)
    {
        char s[32];
        // printf("%d", ct[b]);
        re[b] = re_scramble(ct[b]);
        // printf("%s,", itoa(re[b], s, 2));
    }
    for (int b = 0; b < 32; b++)
    {
        printf("%c", re[b] & 0b01111111);
    }
    // printf("%s", re);
    //  printf("end\n");
    return 0;
}

char switchBits(char c, int p1, int p2)
{
    /*
     * Move the bit in position p1 to position p2, and move the bit
     * that was in position p2 to position p1. Precondition: p1 < p2
     */
    char mask1 = (char)(1 << p1);
    char mask2 = (char)(1 << p2);
    /* char mask3 = (char)(1<<p1<<p2); mask1++; mask1--; */
    char bit1 = (char)(c & mask1);
    char bit2 = (char)(c & mask2);
    /*
     * System.out.println("bit1 " + Integer.toBinaryString(bit1));
     * System.out.println("bit2 " + Integer.toBinaryString(bit2));
     */
    char rest = (char)(c & ~(mask1 | mask2));
    char shift = (char)(p2 - p1);
    char result = (char)((bit1 << shift) | (bit2 >> shift) | rest);
    return result;
}
char re_scramble(char a)
{
    char c = a;
    char s[32];
    printf("0x%x,%s\n", a & 0xff, itoa(c & 0xff, s, 2));
    c = switchBits(c, 6, 7);
    printf("0x%x,%s\n", a & 0xff, itoa(c & 0xff, s, 2));
    c = switchBits(c, 2, 5);
    printf("0x%x,%s\n", a & 0xff, itoa(c & 0xff, s, 2));
    c = switchBits(c, 3, 4);
    printf("0x%x,%s\n", a & 0xff, itoa(c & 0xff, s, 2));
    c = switchBits(c, 0, 1);
    printf("0x%x,%s\n", a & 0xff, itoa(c & 0xff, s, 2));
    c = switchBits(c, 4, 7);
    printf("0x%x,%s\n", a & 0xff, itoa(c & 0xff, s, 2));
    c = switchBits(c, 5, 6);
    printf("0x%x,%s\n", a & 0xff, itoa(c & 0xff, s, 2));
    c = switchBits(c, 0, 3);
    printf("0x%x,%s\n", a & 0xff, itoa(c & 0xff, s, 2));
    c = switchBits(c, 1, 2);
    printf("0x%x,%s\n", a & 0xff, itoa(c & 0xff, s, 2));
    return c;
}