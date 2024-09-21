#include "stdio.h"

unsigned char *s1, s2;

unsigned char data[100];

unsigned char key[9];

int enc;

unsigned int enp[0x1b] = {0xb8,  0x119, 0x13d, 0xb0,  0xc,   0x39b, 0x19d,
                          0x1c1, 0x8c,  0x18,  0x34f, 0x307, 0x337, 0x38,
                          0x135, 0x2c6, 0x44,  0x2c2, 0x31f, 0x8c,  0x2c,
                          0x27e, 0x317, 0x1b9, 0x34,  0x15d, 0x40};

int main() {
  scanf("%s", data);

  enc = 0;
  for (int i = 0; i < 0x1b; i = i + 1) {
    if (((unsigned int)((int)(unsigned int)data[i] >> 6 == enp[i]) |
         (unsigned int)data[i] * 4) != 0) {
      enc = enc + 1;
    }
  }
  if (enc == 0x1b) {
    printf("correct!");
  } else {
    printf("wrong!");
  }

  unsigned int rev1[0x1b];
  unsigned int rev2[0x1b];

  for (int i = 0; i < 0x1b; i = i + 1) {
    rev1[i] = enp[i];
  }

  return 0;
}
