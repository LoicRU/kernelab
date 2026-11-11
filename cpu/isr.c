#include "isr.h"
#include "idt.h"
#include "vga.h"

/* Installe les 32 stubs d'exception dans l'IDT et affiche l'erreur. */

extern void isr0(void), isr1(void), isr2(void), isr3(void);
extern void isr4(void), isr5(void), isr6(void), isr7(void);
extern void isr8(void), isr9(void), isr10(void), isr11(void);
extern void isr12(void), isr13(void), isr14(void), isr15(void);
extern void isr16(void), isr17(void), isr18(void), isr19(void);
extern void isr20(void), isr21(void), isr22(void), isr23(void);
extern void isr24(void), isr25(void), isr26(void), isr27(void);
extern void isr28(void), isr29(void), isr30(void), isr31(void);

static void (*isr_stubs[32])(void) = {
    isr0, isr1, isr2, isr3, isr4, isr5, isr6, isr7,
    isr8, isr9, isr10, isr11, isr12, isr13, isr14, isr15,
    isr16, isr17, isr18, isr19, isr20, isr21, isr22, isr23,
    isr24, isr25, isr26, isr27, isr28, isr29, isr30, isr31,
};

static const char *exception_messages[32] = {
    "Division par zero",
    "Debug",
    "Interruption non masquable",
    "Point d'arret",
    "Overflow",
    "Depassement de limite (BOUND)",
    "Opcode invalide",
    "Peripherique non disponible",
    "Double faute",
    "Depassement de segment (obsolete)",
    "TSS invalide",
    "Segment absent",
    "Faute de pile",
    "Violation generale de protection",
    "Faute de page",
    "Reservee",
    "Erreur FPU",
    "Verification d'alignement",
    "Erreur machine",
    "Exception SIMD",
    "Virtualisation",
    "Reservee", "Reservee", "Reservee", "Reservee",
    "Reservee", "Reservee", "Reservee", "Reservee",
    "Reservee",
    "Securite",
    "Reservee",
};

void isr_install(void)
{
    for (int i = 0; i < 32; i++) {
        idt_set_gate((unsigned char)i, (unsigned int)isr_stubs[i], 0x08, 0x8E);
    }
}

void isr_handler(struct registers *regs)
{
    vga_puts("Exception CPU : ");
    vga_puts(exception_messages[regs->int_no]);
    vga_puts("\n");
    for (;;) {
        __asm__ volatile("cli; hlt");
    }
}
