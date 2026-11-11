#ifndef CPU_ISR_H
#define CPU_ISR_H

/* Gestion des 32 exceptions CPU (ISR 0-31). */

struct registers {
    unsigned int ds;
    unsigned int edi, esi, ebp, esp, ebx, edx, ecx, eax;
    unsigned int int_no, err_code;
    unsigned int eip, cs, eflags, useresp, ss;
};

void isr_install(void);
void isr_handler(struct registers *regs);

#endif
