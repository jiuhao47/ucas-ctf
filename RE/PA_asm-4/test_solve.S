asm4:
	“NeSE_a3112”
	{
		[ebp+8] 'N'=0x4e
		[ebp+9] 'e'=0x65
		[ebp+10] 'S'=0x53
		[ebp+11] 'E'=0x45
		[ebp+12] '_'=0x5f
		[ebp+13] 'a'=0x61
		[ebp+14] '3'=0x33
		[ebp+15] '1'=0x31
		[ebp+16] '1'=0x31
		[ebp+17] '2'=0x32
		[ebp+18] '\0'=0x0
	}
	<+0>:	push   ebp
	<+1>:	mov    ebp,esp
	<+3>:	push   ebx
	在所有的通用寄存器里，EBX是唯一一个没有什么重要的专门用途的寄存器，你可以用它存一个计算过程中的中间变量，或者一个指针等等
	<+4>:	sub    esp,0x10
	esp=esp-16=
	分配空间
	<+7>:	mov    DWORD PTR [ebp-0x10],0x246
	[ebp-16]=0x246:=local16(uint)
	<+14>:	mov    DWORD PTR [ebp-0xc],0x0
	[ebp-12]=0:=
	<+21>:	jmp    0x518 <asm4+27>
	jmp 27
	<+23>:	add    DWORD PTR [ebp-0xc],0x1
	[ebp-12]=[ebp-12]+1=0+1=1
	...
	...
	...
	...

	<+27>:	mov    edx,DWORD PTR [ebp-0xc]
	edx=dword([ebp-12])=0
	<+30>:	mov    eax,DWORD PTR [ebp+0x8]
	eax=0x4553654e
	EAX与AX不是独立的，EAX是32位寄存器，而AX是EAX的低16位。
	<+33>:	add    eax,edx
	eax=eax+edx=0x4553654e
	<+35>:	movzx  eax,BYTE PTR [eax]
	movzx是将源操作数的内容拷贝到目的操作数,并将该值0扩展至16位或者32位。但是它只适用于无符号整数
	eax=byte([0x4553654e])



	<+38>:	test   al,al
	al=0
	Test命令将两个操作数进行逻辑与运算，并根据运算结果设置相关的标志位。
	但是，Test命令的两个操作数不会被改变。运算结果在设置过相关标记位后会被丢弃。
	<+40>:	jne    0x514 <asm4+23>
	标志位ZF=0，则跳转，反正，不跳转
	ZF=1，则与结果为0
	则这里为al=0时，即eax的低8位为0时，不跳转

	jump not equal 23
	以上代码唬人
	总归会执行出去
	且对后面的没有影响

	<+42>:	mov    DWORD PTR [ebp-0x8],0x1
	[ebp-8]=0x1
	<+49>:	jmp    0x587 <asm4+138>
	jmp 138
	<+51>:	mov    edx,DWORD PTR [ebp-0x8]
	edx=[ebp-8]=1
	<+54>:	mov    eax,DWORD PTR [ebp+0x8]
	eax=[ebp+8]="NeSE"=0x4553654e
	<+57>:	add    eax,edx
	eax=eax+edx=0x4553654e+1
	<+59>:	movzx  eax,BYTE PTR [eax]
	eax=byte([eax])
	<+62>:	movsx  edx,al
	edx=带符号al扩展 
	<+65>:	mov    eax,DWORD PTR [ebp-0x8]
	eax=[ebp-8]=1
	<+68>:	lea    ecx,[eax-0x1]
	ecx=eax-1
	<+71>:	mov    eax,DWORD PTR [ebp+0x8]
	eax=[ebp+8]=0x4553654e
	<+74>:	add    eax,ecx
	eax=eax+ecx=eax+1
	<+76>:	movzx  eax,BYTE PTR [eax]
	eax=[eax]
	<+79>:	movsx  eax,al
	eax=[eax]的低八位
	<+82>:	sub    edx,eax
	edx=edx-eax=
	<+84>:	mov    eax,edx
	<+86>:	mov    edx,eax
	<+88>:	mov    eax,DWORD PTR [ebp-0x10]
	<+91>:	lea    ebx,[edx+eax*1]
	<+94>:	mov    eax,DWORD PTR [ebp-0x8]
	<+97>:	lea    edx,[eax+0x1]
	<+100>:	mov    eax,DWORD PTR [ebp+0x8]
	<+103>:	add    eax,edx
	<+105>:	movzx  eax,BYTE PTR [eax]
	<+108>:	movsx  edx,al
	<+111>:	mov    ecx,DWORD PTR [ebp-0x8]
	<+114>:	mov    eax,DWORD PTR [ebp+0x8]
	<+117>:	add    eax,ecx
	<+119>:	movzx  eax,BYTE PTR [eax]
	<+122>:	movsx  eax,al
	<+125>:	sub    edx,eax
	<+127>:	mov    eax,edx
	<+129>:	add    eax,ebx
	<+131>:	mov    DWORD PTR [ebp-0x10],eax
	<+134>:	add    DWORD PTR [ebp-0x8],0x1
	<+138>:	mov    eax,DWORD PTR [ebp-0xc]
	eax=dword([ebp-12])=
	<+141>:	sub    eax,0x1
	eax=eax-1
	<+144>:	cmp    DWORD PTR [ebp-0x8],eax
	cmp [ebp-8] eax 1
	<+147>:	jl     0x530 <asm4+51>
	jump less 51
	<+149>:	mov    eax,DWORD PTR [ebp-0x10]
	<+152>:	add    esp,0x10
	<+155>:	pop    ebx
	<+156>:	pop    ebp
	<+157>:	ret    

