# Étape 2 — GDT, IDT, interruptions, PIC

## Ce qui a été fait

- `cpu/io.h` : accès direct aux ports I/O x86 (`inb`/`outb`), en fonctions
  statiques `inline`.
- `cpu/gdt.{c,h}` + `cpu/gdt_flush.asm` : GDT à 3 entrées (nul, code noyau,
  données noyau), chargement via `lgdt` et rechargement des segments.
- `cpu/idt.{c,h}` + `cpu/idt_flush.asm` : IDT à 256 entrées, chargement via
  `lidt`.
- `cpu/isr.{c,h}` + `cpu/isr_stubs.asm` : les 32 exceptions CPU (0-31), chacune
  avec un stub ASM (généré par macro NASM) qui empile le numéro et saute vers
  un gestionnaire commun ; le handler C affiche le message correspondant.
- `cpu/pic.{c,h}` : remappage du PIC 8259 pour que les IRQ 0-15 deviennent les
  interruptions 32-47 (évite le conflit avec les exceptions CPU).
- `cpu/irq.{c,h}` + `cpu/irq_stubs.asm` : les 16 IRQ matérielles, avec table de
  gestionnaires enregistrables (`irq_register_handler`) et envoi de l'EOI au
  PIC après traitement.
- `kernel/kernel.c` : initialise GDT puis IDT, active les interruptions
  (`sti`), déclenche une interruption logicielle (`int $0x0`) pour vérifier
  que l'ISR répond correctement.
- `Makefile` : règles génériques (`VPATH`, motifs `%.o`) pour compiler
  `boot/`, `kernel/`, `drivers/` et `cpu/` sans dupliquer une règle par
  fichier.

## Pourquoi

Sans IDT ni PIC remappé, la moindre exception (ou IRQ matérielle) fait planter
le CPU (triple faute). C'est un prérequis obligatoire avant le timer, le
clavier, ou tout autre pilote basé sur les interruptions (étape 3).

## Ce qu'on a appris

- Le remappage du PIC est indispensable : par défaut les IRQ 0-15 utilisent
  les vecteurs 8-15, qui recouvrent des exceptions CPU réservées.
- Le stub d'interruption commun doit sauvegarder tous les registres (`pusha`)
  et le segment `ds` avant de repasser en segments noyau, pour pouvoir
  restaurer l'état exact du code interrompu après l'`iret`.
- Les macros NASM (`%macro`) évitent de dupliquer 32 fois le même stub à la
  main tout en gardant chaque fichier `.asm` sous le seuil de lignes du
  linter.
- Test automatisé sous QEMU : capture d'écran via `screendump` (moniteur
  QEMU) pour vérifier que l'exception déclenchée volontairement s'affiche.
