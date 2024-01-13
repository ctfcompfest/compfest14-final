.equ DWORD_SIZE, 8

# Allocate a number of double words on the stack.
.macro stack_allocate n
  daddiu $sp, $sp, -(DWORD_SIZE * \n)
.endm

# Free a number of double words from the stack.
.macro stack_free n
  daddiu $sp, $sp, (DWORD_SIZE * \n)
.endm

# Store the GPR r in the stack at index n.
.macro stack_store_gpr r, n
  sd \r, (DWORD_SIZE * \n)($sp)
.endm

# Load the stack value at index n into GPR r.
.macro stack_load_gpr r, n
  ld \r, (DWORD_SIZE * \n)($sp)
.endm

# Load the stack value at index n into FPR r.
.macro stack_load_fpr r, n
  ldc1 \r, (DWORD_SIZE * \n)($sp)
.endm

# Load the address of the stack element at index n into GPR r.
.macro stack_load_address r, n
  daddiu \r, $sp, (DWORD_SIZE * \n)
.endm

.data
read_string_format: .asciz "%s"
print_string_format: .asciz "%s\n"

.text
.global main
main:
stack_allocate 8
stack_store_gpr $ra, 0

stack_load_address $a0, 1
move $a1, $zero
li $a2, 44
jal memset

dla $a0, read_string_format
stack_load_address $a1, 1
jal scanf
stack_load_address $s0, 1

stack_load_address $t0, 1
dla $t1, main
li $s1, 0

loopxor:
lb $t3, 0($t0)
beq $t3, $zero, exit_loop
lwu $t2, 0($t0)
lwu $t3, 0($t1)
xor $t2, $t2, $t3
sw $t2, 0($t0)
addiu $t0, 4
addiu $t1, 4
lb $t3, 0($t0)
b loopxor

exit_loop:
dla $a0, print_string_format
stack_load_address $a1, 1
jal printf

stack_load_gpr $ra, 0
stack_free 8
jr $ra
