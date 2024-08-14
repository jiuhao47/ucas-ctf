asm1:
	<+0>:	push   ebp
	ebp基址指针寄存器(extended base pointer)，其内存放着一个指针，该指针永远指向系统栈最上面一个栈帧的底部
	它会先取出 ESP 寄存器里面的地址，将其减去4个字节，然后将新地址写入 ESP 寄存器。
	使用减法是因为 Stack 从高位向低位发展
	<+1>:	mov    ebp,esp
	esp栈指针寄存器(extended stack pointer)，其内存放着一个指针，该指针永远指向系统栈最上面一个栈帧的栈顶
	<+3>:	cmp    DWORD PTR [ebp+0x8],0x3fb
	dword   双字 就是四个字节 ptr     pointer缩写 即指针,即取出[ebp+0x8]中的值0x2e0(736)，0x3fb(1019)
	CMP(比较)指令执行从目的操作数中减去源操作数的隐含减法操作，并且不修改任何操作数
	CMP 目的操作数, 源操作数
	标志位 当实际的减法发生时，CMP指令按照计算结果修改溢出、符号、零、进位、辅助进位和奇偶标志位。
	如果比较的是两个无符号数，则零标志位和进位标志位表示的两个操作数之间的关系如下表所示：
	<+10>:	jg     0x512 <asm1+37>
	jg有符号大于则跳转
	<+12>:	cmp    DWORD PTR [ebp+0x8],0x280
	比较0x2e0和0x280，大于
	<+19>:	jne    0x50a <asm1+29>
	JNE	不等跳转(not equal)
	<+21>:	mov    eax,DWORD PTR [ebp+0x8]
	<+24>:	add    eax,0xa
	<+27>:	jmp    0x529 <asm1+60>
	<+29>:	mov    eax,DWORD PTR [ebp+0x8]
	eax=0x2e0
	<+32>:	sub    eax,0xa
	SUB指令：减法 SUB S1 S2 D DSUB S1 S2 D，D+1
	eax=0x2d6
	<+35>:	jmp    0x529 <asm1+60>
	<+37>:	cmp    DWORD PTR [ebp+0x8],0x559
	<+44>:	jne    0x523 <asm1+54>
	<+46>:	mov    eax,DWORD PTR [ebp+0x8]
	<+49>:	sub    eax,0xa
	<+52>:	jmp    0x529 <asm1+60>
	<+54>:	mov    eax,DWORD PTR [ebp+0x8]
	<+57>:	add    eax,0xa
	<+60>:	pop    ebp
	ebp=0x2d6
	<+61>:	ret    
	NeSE{000002d6}
