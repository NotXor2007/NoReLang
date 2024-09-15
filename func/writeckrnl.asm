;written by adam naanaa
;09/09/2024

;writec
;V AMD64 ABI
writeckrnl:
push rbp
mov rbp, rsp
sub rsp, 8
and rsp, 0xffffffffffffffff
mov rdx, rsi
mov rsi, rdi
mov rdi, 0
mov rax, 1
syscall
mov rsp, rbp
pop rbp
ret

