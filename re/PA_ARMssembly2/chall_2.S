	.arch armv8-a
	.file	"chall_2.c"
	.text
	.align	2
	.global	func1
	.type	func1, %function
func1:
	sub	sp, sp, #32
	// space alloc 
	str	w0, [sp, 12]
	str	wzr, [sp, 24]
	// i=0
	str	wzr, [sp, 28]
	// j=0
	b	.L2
.L3:
	ldr	w0, [sp, 24]
	add	w0, w0, 3
	str	w0, [sp, 24]
	//i = i + 3
	ldr	w0, [sp, 28]
	add	w0, w0, 1
	str	w0, [sp, 28]
	//j = j +1
.L2:
	ldr	w1, [sp, 28]
	// j(++)
	ldr	w0, [sp, 12]
	// para(const)
	cmp	w1, w0
	bcc	.L3
	// loop
	ldr	w0, [sp, 24]
	// output： i
	add	sp, sp, 32
	// space free
	ret
	.size	func1, .-func1
	.section	.rodata
	.align	3
.LC0:
	.string	"Result: %ld\n"
	.text
	.align	2
	.global	main
	.type	main, %function
main:
	stp	x29, x30, [sp, -48]!
	add	x29, sp, 0
	str	w0, [x29, 28]
	str	x1, [x29, 16]
	ldr	x0, [x29, 16]
	add	x0, x0, 8
	ldr	x0, [x0]
	bl	atoi
	// 读参数，分空间
	bl	func1
	str	w0, [x29, 44]
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	ldr	w1, [x29, 44]
	bl	printf
	nop
	ldp	x29, x30, [sp], 48
	ret
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
