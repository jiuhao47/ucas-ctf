asm3:
	[ebp+8] 0xd73346ed
	{
		[ebp+8]=ed
		[ebp+9]=46
		[ebp+10]=33
		[ebp+11]=d7
	}
	[ebp+12] 0xd48672ae 
	[ebp+16] 0xd3c8b139 
	<+0>:	push   ebp
	<+1>:	mov    ebp,esp
	<+3>:	xor    eax,eax
	xor异或运算
	eax=0
	<+5>:	mov    ah,BYTE PTR [ebp+0xa]
	小端序：低位字节存入低地址，高位字节存入高地址
	ah=byte([ebp+10])=0x33
	<+8>:	shl    ax,0x10
	低位字节存入低地址，高位字节存入高地址
	AL，AH合并起来是AX，其中，AX是一个16位寄存器，AH就是AX的高字节（高8位），AL是AX的低字节（低8位）
	shl ax 16
	等价于
	ax=0
	ah=0
	shl 逻辑左移，将目的操作数每位左移，
	<+12>:	sub    al,BYTE PTR [ebp+0xc]
	al=al-byte([ebp+12])=al-byte(0xae)=al-10101110=0x52
	<+15>:	add    ah,BYTE PTR [ebp+0xd]
	ah=ah+byte([ebp+13])=ah+byte(0x72)=byte(0x0+0x72)=byte(72)
	<+18>:	xor    ax,WORD PTR [ebp+0x10]
	xor 0x7252 0xb139
	ax=0x7252^0xb139=0xc36b
	<+22>:	nop
	空指令
	<+23>:	pop    ebp
	<+24>:	ret    
	NeSE{0000c36b}

