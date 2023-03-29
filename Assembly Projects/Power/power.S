# *********************************************************************************
# * Program name: pow                                                             *
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
    formatstr: .asciz "%ld" # Scanf

.global my_main
.global my_pow

my_main:
    pushq   %rbp                        # boiler plate
    movq    %rsp, %rbp
    subq    $16, %rsp
    
    movq $0, %rax 
    leaq -8(%rbp), %rsi                 # store the base in this stack location
    leaq formatstr(%rip), %rdi
    call scanf                          # call scanf with the respective arguments
    
    movq $0, %rax  
    leaq -16(%rbp), %rsi                # store the exponent
    leaq formatstr(%rip), %rdi
    call scanf                          # call scanf with the respective arguments

    movq -8(%rbp), %rdi                 # this is the base
    movq -16(%rbp), %rsi                # this is the exponent
    call my_pow

    movq %rax, %rsi                     # this is the computed answer
    movq $0, %rax

    leaq formatstr(%rip), %rdi          # formatted string
    call printf

end:
    movq     $0, %rdi            
    call     exit 

my_pow: 
        pushq   %rbp
        movq    %rsp, %rbp

        subq    $16, %rsp

        movq    %rdi, -8(%rbp)          # base
        movq    %rsi, -16(%rbp)         # exponent
        movq    -8(%rbp), %rax

        jmp     loop1
loop2:
        imulq   -8(%rbp), %rax
        subq    $1, -16(%rbp)

loop1:
        cmpq    $1, -16(%rbp)
        jl exception_one
        jne     loop2   

        addq    $16, %rsp
        popq    %rbp
        ret

exception_one:                      # exception when the exponent is 0
        movq $1, %rax
        addq    $16, %rsp
        popq    %rbp
        ret