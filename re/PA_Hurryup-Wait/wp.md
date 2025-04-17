# Hurryup-Wait

## File Analysis

```shell
$ file svhost.exe
```

svchost.exe: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=c083b0f6ecaeb1517082fb6ed0cd9e3f295ec2cc, stripped

It is actually a elf file not a windows executable.

## Reverse Analysis

Use Ghidra, and we can found it is a ada program.

```c
// throught simple reverse analysis
// rename the vars and functions.
int main(int argc, char *argv, char *envp)
{
  char initialization_data[8];
  gnat_envp = envp;
  gnat_argv = argv;
  gnat_argc = argc;
  __gnat_initialize(initialization_data);
  start();
  key(); // the key function is here
  finish();
  __gnat_finalize();
  return gnat_exit_status;
}
```

Then we analysis the funtion `key`

```c
void key(void)

{
  ada__calendar__delays__delay_for(1000000000000000);
  // this would last for 31709792 year
  // so we need to figure out the rest function's funtionality
  FUN_001023a6();
  FUN_00102136();
  FUN_00102206();
  FUN_0010230a();
  FUN_00102206();
  FUN_0010257a();
  FUN_001028ee();
  FUN_0010240e();
  FUN_001026e6();
  FUN_00102782();
  FUN_001028ee();
  FUN_001023da();
  FUN_0010230a();
  FUN_0010233e();
  FUN_0010226e();
  FUN_001022a2();
  FUN_001023da();
  FUN_001021d2();
  return;
}
```

no exception it looks like this

```c
void FUN_001023a6(void)
{
  ada__text_io__put__4(&DAT_00102ccc,&DAT_00102cb8);
  return;
}
```

It gets a string from the data section and print it out.

```c
void key(void)
{
  ada__calendar__delays__delay_for(1000000000000000);
  d();
  1();
  5();
  a();
  5();
  m();
  _();
  f();
  t();
  w();
  _();
  e();
  a();
  b();
  7();
  8();
  e();
  4();
  return;
}
```

so after rename the function to the string they print out, we can get the flag.
