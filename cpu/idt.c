#include "idt.h"
#include "isr.h"
#include "irq.h"

/* Construit, remplit et charge l'IDT (256 entrees). */

struct idt_entry {
    unsigned short base_low;
    unsigned short selector;
    unsigned char zero;
    unsigned char flags;
    unsigned short base_high;
} __attribute__((packed));

struct idt_ptr {
    unsigned short limit;
    unsigned int base;
} __attribute__((packed));

#define IDT_ENTRIES 256

static struct idt_entry idt[IDT_ENTRIES];
static struct idt_ptr idtp;

extern void idt_flush(unsigned int idt_ptr_addr);

void idt_set_gate(unsigned char num, unsigned int base, unsigned short selector,
                   unsigned char flags)
{
    idt[num].base_low = (unsigned short)(base & 0xFFFF);
    idt[num].base_high = (unsigned short)((base >> 16) & 0xFFFF);
    idt[num].selector = selector;
    idt[num].zero = 0;
    idt[num].flags = flags;
}

void idt_init(void)
{
    idtp.limit = sizeof(idt) - 1;
    idtp.base = (unsigned int)&idt;

    for (int i = 0; i < IDT_ENTRIES; i++) {
        idt_set_gate((unsigned char)i, 0, 0, 0);
    }

    isr_install();
    irq_install();

    idt_flush((unsigned int)&idtp);
}
