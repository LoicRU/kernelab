#include "vga.h"

/* Pilote d'affichage texte VGA 80x25 (mémoire mappée à 0xB8000). */

#define VGA_WIDTH 80
#define VGA_HEIGHT 25
#define VGA_MEMORY ((volatile unsigned short *)0xB8000)
#define VGA_COLOR 0x0F /* texte blanc sur fond noir */

static unsigned int cursor_row = 0;
static unsigned int cursor_col = 0;

static void vga_scroll(void);

void vga_clear(void)
{
    for (unsigned int i = 0; i < VGA_WIDTH * VGA_HEIGHT; i++) {
        VGA_MEMORY[i] = (unsigned short)(' ' | (VGA_COLOR << 8));
    }
    cursor_row = 0;
    cursor_col = 0;
}

void vga_putc(char c)
{
    if (c == '\n') {
        cursor_col = 0;
        cursor_row++;
    } else {
        unsigned int pos = cursor_row * VGA_WIDTH + cursor_col;
        VGA_MEMORY[pos] = (unsigned short)((unsigned char)c | (VGA_COLOR << 8));
        cursor_col++;
        if (cursor_col >= VGA_WIDTH) {
            cursor_col = 0;
            cursor_row++;
        }
    }
    if (cursor_row >= VGA_HEIGHT) {
        vga_scroll();
    }
}

void vga_puts(const char *s)
{
    while (*s) {
        vga_putc(*s);
        s++;
    }
}

static void vga_scroll(void)
{
    for (unsigned int row = 1; row < VGA_HEIGHT; row++) {
        for (unsigned int col = 0; col < VGA_WIDTH; col++) {
            VGA_MEMORY[(row - 1) * VGA_WIDTH + col] = VGA_MEMORY[row * VGA_WIDTH + col];
        }
    }
    for (unsigned int col = 0; col < VGA_WIDTH; col++) {
        VGA_MEMORY[(VGA_HEIGHT - 1) * VGA_WIDTH + col] = (unsigned short)(' ' | (VGA_COLOR << 8));
    }
    cursor_row = VGA_HEIGHT - 1;
}
