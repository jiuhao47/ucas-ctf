	.arch armv8-a @声明目标架构
	.file	"chall.c" @
	.text @可执行代码段（程序段）
	.align	2 @数据对齐指令
	.global	func1 @使fun这个符号（函数名）外部可见
	.type	func1, %function 
		@设置一个符号的属性值
		语法：.type name , description
		description取值如下：
		%function 表示该符号用来表示一个函数名
		%object表示该符号用来表示一个数据对象

		FP：栈顶指针，指向一个栈帧的顶部，当函数发生跳转时，会记录当时的栈的起始位置。
		SP：栈指针（也称为栈底指针），指向栈当前的位置，
		LR：链接寄存器，保存函数返回的地址。
		
		ARMv8架构提供31个通用寄存器，其中W0-W30是32位宽度的通用寄存器，X0-X30是64位宽度的通用寄存器
		W0寄存器是X0寄存器的低32位
func1:
    sub	sp, sp, #16
	str	w0, [sp, 12]
	str	w1, [sp, 8]
	ldr	w1, [sp, 12]
	ldr	w0, [sp, 8]
	cmp	w1, w0
	bls	.L2
	ldr	w0, [sp, 12]
	b	.L3
.L2:
	ldr	w0, [sp, 8]
.L3:
	add	sp, sp, 16
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
	stp	x29, x30, [sp, -48]! @stp 指令是 str 的变种指令，p 可以理解成 pair 的意思，可以同时操作两个寄存器
	add	x29, sp, 0 
	str	x19, [sp, 16]
	str	w0, [x29, 44]
	str	x1, [x29, 32]
	ldr	x0, [x29, 32]
	add	x0, x0, 8
	ldr	x0, [x0]
	bl	atoi
	mov	w19, w0
	ldr	x0, [x29, 32]
	add	x0, x0, 16
	ldr	x0, [x0]
	bl	atoi
	mov	w1, w0
	mov	w0, w19
	bl	func1
	mov	w1, w0
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	bl	printf
	mov	w0, 0
	ldr	x19, [sp, 16]
	ldp	x29, x30, [sp], 48
	ret
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
