#include "pic.h"
#include "io.h"

/* Remappage du PIC 8259 : IRQ 0-15 deviennent les interruptions 32-47. */

#define PIC1_CMD  0x20
#define PIC1_DATA 0x21
#define PIC2_CMD  0xA0
#define PIC2_DATA 0xA1
#define PIC_EOI   0x20

#define ICW1_INIT 0x10
#define ICW1_ICW4 0x01
#define ICW4_8086 0x01

void pic_remap(void)
{
    unsigned char mask1 = inb(PIC1_DATA);
    unsigned char mask2 = inb(PIC2_DATA);

    outb(PIC1_CMD, ICW1_INIT | ICW1_ICW4);
    outb(PIC2_CMD, ICW1_INIT | ICW1_ICW4);

    outb(PIC1_DATA, 32);    /* IRQ 0-7  -> interruptions 32-39 */
    outb(PIC2_DATA, 40);    /* IRQ 8-15 -> interruptions 40-47 */

    outb(PIC1_DATA, 4);     /* signale au maitre la cascade sur IRQ2 */
    outb(PIC2_DATA, 2);     /* indique a l'esclave son identite de cascade */

    outb(PIC1_DATA, ICW4_8086);
    outb(PIC2_DATA, ICW4_8086);

    outb(PIC1_DATA, mask1);
    outb(PIC2_DATA, mask2);
}

void pic_send_eoi(unsigned char irq)
{
    if (irq >= 8) {
        outb(PIC2_CMD, PIC_EOI);
    }
    outb(PIC1_CMD, PIC_EOI);
}
