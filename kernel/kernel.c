#include "vga.h"

/* Point d'entrée du noyau, appelé depuis boot/boot.asm. */

void kmain(void)
{
    vga_clear();
    vga_puts("Kernelab OS\n");
    vga_puts("Boot Multiboot + affichage VGA texte : OK\n");
}
