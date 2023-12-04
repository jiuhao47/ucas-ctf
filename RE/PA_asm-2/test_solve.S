asm2:
	0x4 [ebp+8]
	0x2d [ebp+12]
	<+0>:	push   ebp
	esp=esp-4
	<+1>:	mov    ebp,esp
	<+3>:	sub    esp,0x10
	esp=esp-0x10=esp-16
	分配内存空间
	<+6>:	mov    eax,DWORD PTR [ebp+0xc]
	eax=[ebp+12]=0x2d
	<+9>:	mov    DWORD PTR [ebp-0x4],eax
	[ebp-4]=0x2d
	<+12>:	mov    eax,DWORD PTR [ebp+0x8]
	eax=[ebp+8]=0x4
	<+15>:	mov    DWORD PTR [ebp-0x8],eax
	[ebp-8]=0x4
	<+18>:	jmp    0x50c <asm2+31>
	jmp 31
	<+20>:	add    DWORD PTR [ebp-0x4],0x1
	[ebp-4]=[ebp-4]+1=0x2e
	<+24>:	add    DWORD PTR [ebp-0x8],0xd1
	[ebp-8]=[ebp-8]+0xd1=0x2d+0xd1=0xfe
	<+31>:	cmp    DWORD PTR [ebp-0x8],0x5fa1
	cmp 0x4 0x5fa1 ret <
	
	<+38>:	jle    0x501 <asm2+20>
	jle (less or equal)
	jmp 20
	<+40>:	mov    eax,DWORD PTR [ebp-0x4]
	eax=(0x5fa1-0x4)/0xd1+0x2d+1=0xa3
	<+43>:	leave  
	<+44>:	ret    
	NeSE{000000a3}
