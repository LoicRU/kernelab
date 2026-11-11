#include "vga.h"
#include "gdt.h"
#include "idt.h"

/* Point d'entrée du noyau, appelé depuis boot/boot.asm. */

void kmain(void)
{
    vga_clear();
    vga_puts("Kernelab OS\n");
    vga_puts("Boot Multiboot + affichage VGA texte : OK\n");

    gdt_init();
    idt_init();
    vga_puts("GDT et IDT initialisees, PIC remappe (IRQ 32-47)\n");

    __asm__ volatile("sti");

    vga_puts("Test d'exception (interruption 0) :\n");
    __asm__ volatile("int $0x0");

    for (;;) {
        __asm__ volatile("hlt");
    }
}
