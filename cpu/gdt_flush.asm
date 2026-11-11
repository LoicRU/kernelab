; Charge le registre GDTR et recharge les registres de segment.

section .text
global gdt_flush

gdt_flush:
    mov eax, [esp + 4]
    lgdt [eax]

    mov ax, 0x10        ; selecteur donnees noyau (entree 2)
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    jmp 0x08:.flush      ; selecteur code noyau (entree 1)
.flush:
    ret
