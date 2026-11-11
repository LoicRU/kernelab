#ifndef CPU_IRQ_H
#define CPU_IRQ_H

#include "isr.h"

/* Dispatch des 16 IRQ materielles (32-47) vers des gestionnaires. */

typedef void (*irq_handler_t)(struct registers *regs);

void irq_install(void);
void irq_register_handler(unsigned char irq, irq_handler_t handler);
void irq_handler(struct registers *regs);

#endif
