#ifndef DRIVERS_VGA_H
#define DRIVERS_VGA_H

/* Pilote d'affichage texte VGA (mode 80x25, mémoire à 0xB8000). */

void vga_clear(void);
void vga_putc(char c);
void vga_puts(const char *s);

#endif
