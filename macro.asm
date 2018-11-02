%macro addition 2
	mov eax,%1
	mov ebx,%2
	add eax,ebx
%endmacro
%macro subtraction 2
	mov eax,%1
	mov ebx,%2
	sub eax,ebx
%endmacro
%macro addition 2
	mov eax,%1
	mov edx,%2
	add eax,edx
%endmacro
section .data
	msg db "%d",10,0
section .text
	global main
	extern printf
main:	addition 10,20
	push eax
	push msg
	call printf
	add esp,8
	subtraction 100,20
	push eax
	push msg
	call printf
	add esp,8
