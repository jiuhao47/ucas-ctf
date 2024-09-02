#include <stdio.h>
#include <stdlib.h>
long input = 2907278761;
long func1(long);
long func2(long);
long func3(long);
long func4(long);
long func5(long);
long func6(long);
long func7(long);
long func8(long);

/* func1:
        stp	x29, x30, [sp, -32]!
        add	x29, sp, 0
        str	w0, [x29, 28]
        ldr	w0, [x29, 28]
        cmp	w0, 100
        bls	.L2
        ldr	w0, [x29, 28]
        add	w0, w0, 100
        bl	func2
        b	.L3
.L2:
        ldr	w0, [x29, 28]
        bl	func3
.L3:
        ldp	x29, x30, [sp], 32
        ret
        .size	func1, .-func1
        .align	2
        .global	func2
        .type	func2, %function
*/
long func1(long x) {
  if (x > 100) {
    x = func2(x + 100);
  } else {
    x = func3(x);
  }
  return x;
}
/* func2:
        stp	x29, x30, [sp, -32]!
        add	x29, sp, 0
        str	w0, [x29, 28]
        ldr	w0, [x29, 28]
        cmp	w0, 499
        bhi	.L5
        ldr	w0, [x29, 28]
        sub	w0, w0, #86
        bl	func4
        b	.L6
.L5:
        ldr	w0, [x29, 28]
        add	w0, w0, 13
        bl	func5
.L6:
        ldp	x29, x30, [sp], 32
        ret
        .size	func2, .-func2
        .align	2
        .global	func3
        .type	func3, %function
*/
long func2(long x) {
  if (x > 499) {
    x = func5(x + 13);
  } else {
    x = func4(x - 86);
  }
  return x;
}
/*
func3:
        stp	x29, x30, [sp, -32]!
        add	x29, sp, 0
        str	w0, [x29, 28]
        ldr	w0, [x29, 28]
        bl	func7
        ldp	x29, x30, [sp], 32
        ret
        .size	func3, .-func3
        .align	2
        .global	func4
        .type	func4, %function
*/
long func3(long x) {
  x = func7(x);
  return x;
}

/*
func4:
        stp	x29, x30, [sp, -48]!
        add	x29, sp, 0
        str	w0, [x29, 28]
        mov	w0, 17
        str	w0, [x29, 44]
        ldr	w0, [x29, 44]
        bl	func1
        str	w0, [x29, 44]
        ldr	w0, [x29, 28]
        ldp	x29, x30, [sp], 48
        ret
        .size	func4, .-func4
        .align	2
        .global	func5
        .type	func5, %function
*/
long func4(long x) {
  x = func1(17);
  return x;
}

/* func5:
        stp	x29, x30, [sp, -32]!
        add	x29, sp, 0
        str	w0, [x29, 28]
        ldr	w0, [x29, 28]
        bl	func8
        str	w0, [x29, 28]
        ldr	w0, [x29, 28]
        ldp	x29, x30, [sp], 32
        ret
        .size	func5, .-func5
        .align	2
        .global	func6
        .type	func6, %function */
long func5(long x) {
  x = func8(x);
  return x;
}

/* func6:
        sub	sp, sp, #32
        str	w0, [sp, 12]
        mov	w0, 314
        str	w0, [sp, 24]
        mov	w0, 1932
        str	w0, [sp, 28]
        str	wzr, [sp, 20]
        str	wzr, [sp, 20]
        b	.L14
.L15:
        ldr	w1, [sp, 28]
        mov	w0, 800
        mul	w0, w1, w0
        ldr	w1, [sp, 24]
        udiv	w2, w0, w1
        ldr	w1, [sp, 24]
        mul	w1, w2, w1
        sub	w0, w0, w1
        str	w0, [sp, 12]
        ldr	w0, [sp, 20]
        add	w0, w0, 1
        str	w0, [sp, 20]
.L14:
        ldr	w0, [sp, 20]
        cmp	w0, 899
        bls	.L15
        ldr	w0, [sp, 12]
        add	sp, sp, 32
        ret
        .size	func6, .-func6
        .align	2
        .global	func7
        .type	func7, %function */
long func6(long x) {
  long a = 314;
  long b = 1932;
  long c = 0;
  for (int i = 0; i < 900; i++) {
    c = x * 800 / b;
    x -= c * b;
  }
  return x;
}

/* func7:
        sub	sp, sp, #16
        str	w0, [sp, 12]
        ldr	w0, [sp, 12]
        cmp	w0, 100
        bls	.L18
        ldr	w0, [sp, 12]
        b	.L19
.L18:
        mov	w0, 7
.L19:
        add	sp, sp, 16
        ret
        .size	func7, .-func7
        .align	2
        .global	func8
        .type	func8, %function */
long func7(long x) {
  if (x > 100) {
    x = 7;
  }
  return x;
}

/* func8:
        sub	sp, sp, #16
        str	w0, [sp, 12]
        ldr	w0, [sp, 12]
        add	w0, w0, 2
        add	sp, sp, 16
        ret
        .size	func8, .-func8
        .section	.rodata
        .align	3
.LC0:
        .string	"Result: %ld\n"
        .text
        .align	2
        .global	main
        .type	main, %function */
long func8(long x) { return x + 2; }

/* main:
        stp	x29, x30, [sp, -48]!
        add	x29, sp, 0
        str	w0, [x29, 28]
        str	x1, [x29, 16]
        ldr	x0, [x29, 16]
        add	x0, x0, 8
        ldr	x0, [x0]
        bl	atoi
        str	w0, [x29, 44]
        ldr	w0, [x29, 44]
        bl	func1
        mov	w1, w0
        adrp	x0, .LC0
        add	x0, x0, :lo12:.LC0
        bl	printf
        nop
        ldp	x29, x30, [sp], 48
        ret
        .size	main, .-main
        .ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
        .section	.note.GNU-stack,"",@progbits */
int main() {
  printf("Result: %lx\n", func1(input));
  return 0;
}

