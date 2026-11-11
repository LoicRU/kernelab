# kernelab — OS from scratch (apprentissage + portfolio)

Projet de Loïc : écrire un petit OS x86 (32 bits) en C + ASM, bootable avec GRUB (Multiboot),
testé avec QEMU. Objectif : apprendre et avoir un projet propre à montrer dans un portfolio.

## Règles de travail (IMPORTANT)

- Réponds en français, de façon courte et précise.
- **Avant de coder**, donne un résumé bref et précis de ce que tu vas faire, puis attends « go ».
- **Ne lance jamais de git qui modifie l'état** (add, commit, push, reset...). Loïc commit lui-même.
- À la fin de chaque étape, donne le(s) **nom(s) de commit** à utiliser
  (Conventional Commits en français : `feat(vga): ...`, `chore(lint): ...`).
- Une étape = une feature = un commit. Ne mélange pas deux étapes.
- Avant de dire « terminé » : `make lint` doit afficher OK et l'OS doit booter dans QEMU
  (`make run` ou test automatisé `make test` quand il existe).
- Commentaires du code et documentation en français.

## Stack

- C (`gcc -m32 -ffreestanding -fno-pie -fno-stack-protector -nostdlib`, ou cross-compiler `i686-elf-gcc`)
- ASM : NASM (format elf32)
- Bootloader : GRUB (Multiboot), image avec `grub-mkrescue`
- Émulateur : `qemu-system-i386`
- Paquets WSL/Ubuntu : `build-essential gcc-multilib nasm qemu-system-x86 grub-pc-bin xorriso mtools python3`

## Structure cible

```
kernelab/
├── Makefile            # all, run, test, lint, clean
├── linker.ld
├── CLAUDE.md
├── README.md           # à la fin : présentation portfolio (+ capture/GIF)
├── docs/               # architecture, une page par étape
├── tools/              # lint.py, lint.conf, lintlib/
├── boot/               # boot.asm (en-tête Multiboot, entrée)
├── kernel/             # kernel.c (kmain) + core
├── drivers/            # vga, keyboard, timer, ata...
├── cpu/                # gdt, idt, isr, irq, pic
├── mm/                 # paging, heap (kmalloc)
├── proc/               # processus, scheduler, syscalls
├── fs/                 # système de fichiers
└── shell/              # shell interactif
```

## Règles de lint (une feature = un fichier)

Seuils dans `tools/lint.conf` :

| Règle | Seuil |
|---|---|
| Lignes par fichier (.c .h .asm .S .py .ld) | 200 max |
| Lignes par fonction (C) | 40 max |
| Fonctions publiques (non `static`) par .c | 8 max |
| Longueur de ligne | 100 max |

Autres règles : chaque `.c` a un `.h` du même nom (sauf `kernel.c`), garde `#ifndef/#define`
dans chaque `.h`, noms de fichiers et de fonctions en `snake_case`, pas d'espaces en fin de
ligne, TODO obligatoirement étiqueté `TODO(nom)`.

### Étape 0 — créer le linter (si `tools/lint.py` n'existe pas)

Linter Python 3 sans dépendance, lancé par `make lint` (code retour ≠ 0 si erreur), qui respecte
lui-même ses règles (donc découpé en petits modules dans `tools/lintlib/`) :

- `tools/lint.py` : point d'entrée mince ; `--root` et `--conf` en options.
- `tools/lint.conf` : `clé = valeur`, `#` commentaires ; listes séparées par des virgules ;
  clés : `max_file_lines`, `max_function_lines`, `max_public_functions`, `max_line_length`,
  `header_exempt`, `exclude_dirs` (`.git, build, __pycache__, iso`), `extensions`.
- `lintlib/` : `config.py`, `issue.py` (path, line, rule, msg), `cstrip.py` (blanchit
  commentaires, chaînes et préprocesseur en gardant les retours à la ligne), `cfuncs.py`
  (détecte les définitions de fonctions par comptage d'accolades au niveau 0, avec nom, ligne
  de début/fin et `static`), `source.py`, `rules_text.py` (file-length, line-length,
  trailing-ws, todo-tag, file-name), `rules_c.py` (function-length, public-functions,
  function-name, header-guard, header-pair), `runner.py`.
- Sortie : `chemin:ligne: [règle] message`, puis `lint : N fichier(s) analysé(s), OK|N erreur(s)`.
- Ajouter `.gitignore` (`build/ iso/ *.o *.bin *.iso __pycache__/`).
- Commit proposé : `chore(lint): ajoute le linter (taille, une feature par fichier, style)`

## Feuille de route (un commit par étape)

1. **Boot + VGA** : Makefile, `boot/boot.asm` (Multiboot), `kernel/kernel.c`, `drivers/vga.c`,
   `linker.ld`, `make run`. Commit : `feat(boot): démarrage Multiboot et affichage VGA texte`
2. **GDT, IDT, interruptions, PIC** (`cpu/`)
3. **Timer (PIT) et clavier** (`drivers/`)
4. **Mémoire** : paging + heap `kmalloc/kfree` (`mm/`)
5. **Processus et ordonnanceur** : coopératif puis préemptif (`proc/`)
6. **Syscalls et mode utilisateur**
7. **Disque ATA + système de fichiers simple** (`drivers/`, `fs/`)
8. **Shell interactif** : `help`, `ls`, `cat`, `ps`, `clear`, `reboot` (`shell/`)
9. **Portfolio** : README, `docs/architecture.md`, capture/GIF, tests `make test` sous QEMU

## Définition de « terminé » pour une étape

- `make lint` → OK
- `make run` boote et la nouvelle feature est visible dans QEMU
- Une page `docs/etape-N.md` courte (ce qui a été fait, pourquoi, ce qu'on a appris)
- Noms de commit proposés à Loïc (il commit lui-même)
