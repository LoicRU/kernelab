#ifndef CPU_IDT_H
#define CPU_IDT_H

/* Table des descripteurs d'interruption (IDT). */

void idt_init(void);
void idt_set_gate(unsigned char num, unsigned int base, unsigned short selector,
                   unsigned char flags);

#endif
