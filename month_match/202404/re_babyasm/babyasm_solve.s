//已知输入为0x20230417，请你解出输出吧^.^
//flag为8位16进制数。例如，若你解出答案为0x5201314，则请提交"flag{05201314}"
//Stack
/*
	
	-8:91
	-4:26
	 0:rbp
	16:0x20230417
	 
*/



babyasm:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	//空间
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR -4[rbp], 26
	mov	DWORD PTR -8[rbp], 91
	jmp	.L4
.L5:
	sal	DWORD PTR 16[rbp], 2
	//0x20230417*2
	add	DWORD PTR 16[rbp], 5
	//0x20230417*2+5
	sar	DWORD PTR 16[rbp], 4
	//0x20230417*2+5/16
	sub	DWORD PTR 16[rbp], 11
	//0x20230417*2+5/16-11
	xor	DWORD PTR 16[rbp], 269029892
	//0x20230417*2+5/16-11^269029892
	add	DWORD PTR -4[rbp], 13
.L4:
	mov	eax, DWORD PTR -8[rbp]
	//eax=91
	cdq
	idiv	DWORD PTR -4[rbp]
	//91/26
	mov	eax, edx
	//eax=91%26
	test	eax, eax
	//
	jne	.L5
	mov	eax, DWORD PTR 16[rbp]
	

	add	rsp, 16
	pop	rbp
	ret
