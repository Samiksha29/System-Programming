section .data
	num1 dd 18
	num2 dd 20
	msg2 db "sum is ="
section .bss
	res resd 1
section .text 
	global main
	extern printf
main:	mov eax,10
	mov ebx,60
	add eax,ebx
	push eax
	push dword[msg2]
	call printf
	add esp,8
