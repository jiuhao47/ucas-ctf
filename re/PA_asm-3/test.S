asm3:
	<+0>:	push   ebp
	<+1>:	mov    ebp,esp
	<+3>:	xor    eax,eax
	<+5>:	mov    ah,BYTE PTR [ebp+0xa]
	<+8>:	shl    ax,0x10
	<+12>:	sub    al,BYTE PTR [ebp+0xc]
	<+15>:	add    ah,BYTE PTR [ebp+0xd]
	<+18>:	xor    ax,WORD PTR [ebp+0x10]
	<+22>:	nop
	<+23>:	pop    ebp
	<+24>:	ret    

