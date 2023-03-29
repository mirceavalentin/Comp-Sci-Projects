# *********************************************************************************
# * Program name: inout                                                           *
# * Description :                                                                 *
# *********************************************************************************

#ifndef MACOS
.ifndef CODEGRADE
    .global main
    main: jmp my_main
.endif
#else
    .global _main
    _main: jmp my_main
    printf: jmp _printf
    scanf: jmp _scanf
    exit: jmp _exit
#endif

.text
        formatstr: .asciz "%ld";

.global my_main                     # make my_main accessible globally
.global my_increment                # make my_increment accessible globally

my_main:
        pushq   %rbp                # boiler plate
	movq    %rsp, %rbp   

        call    inout                         
end:
        movq     $0, %rdi            
        call     exit  

inout:
        pushq   %rbp                 # store the caller's base pointer
	movq    %rsp, %rbp    

        subq $16, %rsp               # allign stack
        

        movq $0, %rax 
        leaq formatstr(%rip), %rdi
        leaq -8(%rbp), %rsi
        call scanf

        movq    -8(%rbp), %rdi
        call    my_increment
        
        movq %rax, %rdx
        movq $0, %rax 
        movq %rdx, %rsi
        leaq formatstr(%rip), %rdi
        call printf

        movq %rbp , %rsp             # epilogue: clear local variables from stack .
        popq %rbp                    # restore caller’ s base pointer .
        ret


my_increment:
        pushq   %rbp                 # store the caller's base pointer
	movq    %rsp, %rbp    

        incq %rdi

        movq %rdi, %rax

        movq %rbp, %rsp              # epilogue: clear local variables from stack .
        popq %rbp                    # restore caller’ s base pointer .
        ret


    