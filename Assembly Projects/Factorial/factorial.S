# *********************************************************************************
# * Program name: factorial                                                       *
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
    formatstr: .asciz "%ld"             # scanf

.global my_main
.global factorial

my_main:
    pushq   %rbp                        # boiler plate
    movq    %rsp, %rbp
    subq    $16, %rsp

    movq $0, %rax 
    leaq -8(%rbp), %rsi                 # get number
    leaq formatstr(%rip), %rdi
    call scanf

    movq -8(%rbp), %rdi                 # result
    call factorial
   
    movq %rax, %rsi                     # result into sec arg
    movq	$0, %rax
    leaq formatstr(%rip), %rdi          # first arg formatstr
    call printf

end:
    movq     $0, %rdi            
    call     exit 

factorial:
        pushq   %rbp                    # boiler plate
        movq    %rsp, %rbp
        subq    $16, %rsp

        movq    %rdi, -8(%rbp)

        cmpq    $1, -8(%rbp)
        jle     factorial_base_case
        jmp     factorial_recursive

factorial_recursive:
        movq    -8(%rbp), %rax
        decq    %rax
        movq    %rax, %rdi

        call    factorial
        movq    %rax, -8(%rbp)
        imulq   -8(%rbp), %rax

        addq    $16, %rsp
        popq    %rbp
        ret

factorial_base_case:
        movq $1, %rax   
        addq    $16, %rsp
        popq    %rbp
        ret
