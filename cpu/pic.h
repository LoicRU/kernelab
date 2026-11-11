#ifndef CPU_PIC_H
#define CPU_PIC_H

/* Controleur d'interruptions programmable 8259 (PIC). */

void pic_remap(void);
void pic_send_eoi(unsigned char irq);

#endif
