; Point d'entrée du noyau : en-tête Multiboot et démarrage.
; Le bootloader (GRUB) cherche cet en-tête puis saute à _start.

MAGIC    equ 0x1BADB002
FLAGS    equ 0x0
CHECKSUM equ -(MAGIC + FLAGS)

section .multiboot
align 4
    dd MAGIC
    dd FLAGS
    dd CHECKSUM

section .bss
align 16
stack_bottom:
    resb 16384
stack_top:

section .text
global _start
extern kmain

_start:
    mov esp, stack_top
    call kmain
    cli
.hang:
    hlt
    jmp .hang
