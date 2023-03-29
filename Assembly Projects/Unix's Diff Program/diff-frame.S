# *********************************************************************************
# * Program name: diff                                                            *
# * Description : Line-by-line diff                                               *
# *********************************************************************************

#ifdef MACOS
    .global _diff
    _diff: jmp diff
    fgets: jmp _fgets
    fread: jmp _fread
    fprintf: jmp _fprintf
    fscanf: jmp _fscanf
    printf: jmp _printf
    strcasecmp: jmp _strcasecmp
    strcmp: jmp _strcmp
    strcpy: jmp _strcpy
    strlen: jmp _strlen
    strncasecmp: jmp _strncasecmp
    strncmp: jmp _strncmp 
    strncpy: jmp _strncpy
    strnlen: jmp _strnlen
    exit: jmp _exit
#endif

.data
    I_FLAG:     .quad 0
    B_FLAG:     .quad 0

.bss
    string1: .skip 1024
    string2: .skip 1024

.text

changestring: 
            .ascii "%dc%d\n"
		    .ascii "< %s"
		    .ascii "---\n"
		    .asciz "> %s"

changestring_exeption: 
            .ascii "%dc%d\n"
		    .ascii "< %s\n"
		    .ascii "---\n"
		    .asciz "> %s"

.global diff

# ************************************************************************
# * Subroutine: diff
# * Description: A simplified line-by-line implementation of diff
# * Specification: int diff(FILE *a, FILE *b, bool i_flag, bool B_flag);         
# ************************************************************************
diff:
    pushq   %rbp
    movq    %rsp, %rbp  
    subq    $32, %rsp

    movq    %rdi, -8(%rbp)          # create a pointer for file a
    movq    %rsi, -16(%rbp)         # create a pointer for file b

    movq    %rdx, I_FLAG(%rip)      # store i flag
    movq    %rcx, B_FLAG(%rip)      # store b flag

    call    compare_routine

    movq    $0, %rdi
    leave
    call    exit

compare_routine:
    pushq   %rbp
    movq    %rsp, %rbp  
    subq    $32, %rsp
    
    movq    %rdi, -8(%rbp)         
    movq    %rsi, -16(%rbp)         

    movq    $0, %r15         
    
    pushq    %r15                   # initialise other registers
    pushq    %r14
    pushq    %r13

compare_loop:
    leaq    string1(%rip), %rdi     # where it should place the string
    movq    $1024, %rsi             # each line can be a max of 1024
    movq    -8(%rbp), %rdx          # file pointer
    call    fgets                   # call fgets that gets the string line

    cmpq    $0, %rax                # if it's 0, the line is empty
    je      end_loop

    movq    %rax, -24(%rbp)         # we move them to r13 because we need the rax to be empty
    movq    -24(%rbp), %r13

    leaq    string2(%rip), %rdi     # where it should place the string
    movq    $1024 , %rsi            # each line can be a max of 1024
    movq    -16(%rbp), %rdx         # file pointer
    call    fgets                   # call fgets that gets the string line

    cmpq    $0, %rax
    je      end_loop

    movq    %rax, -32(%rbp)         # we move them to r14 because we need the rax to be empty
    movq    -32(%rbp), %r14

    incq    %r15                    # we increment the counter

    jmp     check_i_flag

    jmp     compare_loop

check_i_flag:
    cmpq    $1, I_FLAG(%rip)       # we check the value of the i flag
    je      check_b_flag           # if i is 0 we jump to check the b flag
    cmpq    $1, B_FLAG(%rip)       # we check the value of the b flag
    je      b_flag_case            # if b is 1

    jmp     no_flag_case           # if i and b are disabled 

check_b_flag:
    cmpq    $1, B_FLAG(%rip)       # we check the b flag
    je      both_flag_case 
    jne     i_flag_case

i_flag_case:                       # only i is enabled
    movq    %r13, %rdi             # strcasecmp takes rdi and rsi as arguments
    movq    %r14, %rsi          
    call    strcasecmp             # we call string compare without capitalization  

    cmpq    $0, %rax               # if rax is 0 the lines are identical
    je      compare_loop

    jmp     print_loop             # lines are not the same so we jump to the printing loop

b_flag_case:                       # only b is enabled
    movq    %r13, %rdi             # strlen takes rdi and rsi
    movq    %r14, %rsi             # we use strlen because strlen calculates the lenght of the string
    call    strlen          

    cmpq    $0, %rax               # if rax is 0 the line is empty
    jne     compare_loop

    jmp     print_loop             # we print

both_flag_case:                    # both i and b are enabled
    movq    %r13, %rdi             # strcasecmp takes rdi and rsi
    movq    %r14, %rsi          
    call    strcasecmp             # strcasecmp compares with case insensitivity

    cmpq    $0, %rax               # if rax is 0 then the lines are different and we print
    jne     print_loop

    movq    %r13, %rdi             # strlen takes rdi and rsi
    movq    %r14, %rsi             # we use strlen because strlen calculates the lenght of the string
    call    strlen          

    cmpq    $0, %rax               # if rax is 0 the line is empty
    jne     compare_loop

    jmp     print_loop             # we print

no_flag_case:
    movq    -24(%rbp), %rdi        # both i and b flags are disabled
    movq    -32(%rbp) , %rsi
    call    strcmp                 # strcmp compares with case sensitivity

    cmpq    $0, %rax               # if rax is not equal to 0 the lines are different so we print
    jne     print_loop

    jmp     compare_loop           # otherwise we jump back to the loop

end_loop:
    popq    %r13                   # we pop the registers so we don't get a segmentation error
    popq    %r14
    popq    %r15
    leave 
    ret

print_loop:
    movq    %r13, %rdi

check_new_line:                    # this is an exeption for the first test because it has a newline
    cmpq    $0, (%rdi)              
    je      print_with_newline

    cmpq    $0x0a, (%rdi)           
    je      print_without_newline   # we check if there is a

    incq    %rdi
    jmp     check_new_line

print_without_newline:
    leaq    changestring(%rip), %rdi    
    movq    %r15, %rsi            # counter x1  
    movq    %r15, %rdx            # counter x2                   
    movq    %r13, %rcx            # string 1         
    movq    %r14, %r8             # string 2                     
    movq    $0, %rax
    call    printf                # printf takes 5 arguments. The 2 strings, the counter x2 and the changestring

    jmp     compare_loop

print_with_newline:               # this loop is for the exeption where we have a newline at the beggining (test 1)
    leaq    changestring_exeption(%rip), %rdi    
    movq    %r15, %rsi                      
    movq    %r15, %rdx                      
    movq    %r13, %rcx                     
    movq    %r14, %r8                       
    movq    $0, %rax
    call    printf                # printf takes 5 arguments. The 2 strings, the counter x2 and the changestring

    jmp     compare_loop          # we jump back to the loop