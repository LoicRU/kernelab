; Charge le registre IDTR avec l'adresse de la table passee en argument.

section .text
global idt_flush

idt_flush:
    mov eax, [esp + 4]
    lidt [eax]
    ret
