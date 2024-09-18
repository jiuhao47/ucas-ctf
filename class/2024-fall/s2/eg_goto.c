#include <stdio.h>
int main() {
  for (int i = 0; i < 10; i++) {
    if (i == 5) {
      goto end;
    }
    printf("%d\n", i);
  }
end:
  printf("End");
}
