#include "irq.h"
#include "idt.h"
#include "pic.h"

/* Installe les stubs d'IRQ et route chaque IRQ vers son gestionnaire. */

extern void irq0(void), irq1(void), irq2(void), irq3(void);
extern void irq4(void), irq5(void), irq6(void), irq7(void);
extern void irq8(void), irq9(void), irq10(void), irq11(void);
extern void irq12(void), irq13(void), irq14(void), irq15(void);

static void (*irq_stubs[16])(void) = {
    irq0, irq1, irq2, irq3, irq4, irq5, irq6, irq7,
    irq8, irq9, irq10, irq11, irq12, irq13, irq14, irq15,
};

static irq_handler_t handlers[16];

void irq_install(void)
{
    pic_remap();
    for (int i = 0; i < 16; i++) {
        idt_set_gate((unsigned char)(32 + i), (unsigned int)irq_stubs[i], 0x08, 0x8E);
    }
}

void irq_register_handler(unsigned char irq, irq_handler_t handler)
{
    handlers[irq] = handler;
}

void irq_handler(struct registers *regs)
{
    unsigned char irq = (unsigned char)(regs->int_no - 32);

    if (handlers[irq]) {
        handlers[irq](regs);
    }

    pic_send_eoi(irq);
}
