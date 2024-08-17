#include <stdio.h>
char string_constant [100]= "A_b1t_0f_b1t_sh1fTiNg_dc80e28124";
int main()
{
  for (int i=0;i<100;i++)
  {
    char temp [100];
    for(int j =0;j<100;j++)
    {
      temp[j]= string_constant[j] + i;
      printf("%c",temp[j]);
    }
    printf("\n");
  }
}
