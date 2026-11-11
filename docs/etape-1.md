# Étape 1 — Boot Multiboot et affichage VGA texte

## Ce qui a été fait

- `boot/boot.asm` : en-tête Multiboot (magic, flags, checksum), pile de 16 Ko,
  point d'entrée `_start` qui initialise `esp` puis appelle `kmain`.
- `kernel/kernel.c` : `kmain()` efface l'écran et affiche un message de bienvenue.
- `drivers/vga.c` / `drivers/vga.h` : pilote texte VGA 80x25 (écriture directe
  dans la mémoire à `0xB8000`), avec `vga_clear`, `vga_putc`, `vga_puts` et un
  défilement (`vga_scroll`) quand l'écran est plein.
- `linker.ld` : place le noyau à 1 Mo, sections `.text`/`.rodata`/`.data`/`.bss`.
- `boot/grub.cfg` : configuration GRUB pour démarrer `kernelab.bin` en Multiboot.
- `Makefile` : cibles `all` (compile + link), `iso` (image bootable avec
  `grub-mkrescue`), `run` (lance QEMU).

## Pourquoi

Multiboot évite d'écrire un bootloader bas niveau soi-même : GRUB charge le
noyau en mode protégé 32 bits et saute directement à `_start`. Le VGA texte
est le moyen le plus simple de vérifier qu'un noyau tourne réellement, avant
d'avoir des interruptions ou un clavier.

## Ce qu'on a appris

- Le format Multiboot 1 ne demande qu'un en-tête de 12 octets (magic, flags,
  checksum) aligné sur 4 octets, placé tôt dans le binaire.
- `ld` avec un script de link personnalisé permet de contrôler précisément
  l'adresse de chargement (ici 1 Mo, convention Multiboot).
- Test automatisé sous QEMU : lancer avec `-display none -monitor stdio` et
  envoyer `screendump` via le moniteur permet de vérifier le contenu affiché
  sans interface graphique.
