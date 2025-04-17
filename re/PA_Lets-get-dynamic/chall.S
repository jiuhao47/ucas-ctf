	.file	"chall.c"
	.text
	.section	.rodata
	.align 8
.LC0:
	.string	"Correct! You entered the flag."
.LC1:
	.string	"No, that's not right."
	.text
	.globl	main
	.type	main, @function
main:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$296, %rsp
	.cfi_offset 3, -24
	movl	%edi, -292(%rbp)
	movq	%rsi, -304(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -24(%rbp)
	xorl	%eax, %eax
	movabsq	$3913356094601673258, %rax
	movabsq	$6478272586731273419, %rdx
	movq	%rax, -144(%rbp)
	movq	%rdx, -136(%rbp)
	movabsq	$-1748037878477762649, %rax
	movabsq	$4279356992215022931, %rdx
	movq	%rax, -128(%rbp)
	movq	%rdx, -120(%rbp)
	movabsq	$-7229749860270763735, %rax
	movabsq	$-6940086526098425816, %rdx
	movq	%rax, -112(%rbp)
	movq	%rdx, -104(%rbp)
	movw	$97, -96(%rbp)
	movabsq	$6214777055764401527, %rax
	movabsq	$8184225536171504527, %rdx
	movq	%rax, -80(%rbp)
	movq	%rdx, -72(%rbp)
	movabsq	$-8364134581669616439, %rax
	movabsq	$5916610601309242417, %rdx
	movq	%rax, -64(%rbp)
	movq	%rdx, -56(%rbp)
	movabsq	$-2598080388612165765, %rax
	movabsq	$-4252370736625094538, %rdx
	movq	%rax, -48(%rbp)
	movq	%rdx, -40(%rbp)
	movw	$63, -32(%rbp)
	movq	stdin(%rip), %rdx
	leaq	-208(%rbp), %rax
	movl	$49, %esi
	movq	%rax, %rdi
	call	fgets@PLT
	movl	$0, -276(%rbp)
	jmp	.L2
.L3:
	movl	-276(%rbp), %eax
	cltq
	movzbl	-144(%rbp,%rax), %edx
	movl	-276(%rbp), %eax
	cltq
	movzbl	-80(%rbp,%rax), %eax
	xorl	%eax, %edx
	movl	-276(%rbp), %eax
	xorl	%edx, %eax
	xorl	$19, %eax
	movl	%eax, %edx
	movl	-276(%rbp), %eax
	cltq
	movb	%dl, -272(%rbp,%rax)
	addl	$1, -276(%rbp)
.L2:
	movl	-276(%rbp), %eax
	movslq	%eax, %rbx
	leaq	-144(%rbp), %rax
	movq	%rax, %rdi
	call	strlen@PLT
	cmpq	%rax, %rbx
	jb	.L3
	leaq	-272(%rbp), %rcx
	leaq	-208(%rbp), %rax
	movl	$49, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	memcmp@PLT
	testl	%eax, %eax
	je	.L4
	leaq	.LC0(%rip), %rdi
	call	puts@PLT
	movl	$0, %eax
	jmp	.L6
.L4:
	leaq	.LC1(%rip), %rdi
	call	puts@PLT
	movl	$1, %eax
.L6:
	movq	-24(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L7
	call	__stack_chk_fail@PLT
.L7:
	addq	$296, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
