CC      = gcc
ASM     = nasm
LD      = ld
CFLAGS  = -m32 -ffreestanding -fno-pie -fno-stack-protector -nostdlib \
          -Wall -Wextra -std=gnu11 -Idrivers -Icpu -Ikernel
ASFLAGS = -f elf32
LDFLAGS = -m elf_i386 -T linker.ld

BUILD  = build
ISODIR = iso
VPATH  = boot kernel drivers cpu

C_SRCS   = kernel.c vga.c gdt.c idt.c isr.c irq.c pic.c
ASM_SRCS = boot.asm gdt_flush.asm idt_flush.asm isr_stubs.asm irq_stubs.asm
HEADERS  = $(wildcard drivers/*.h cpu/*.h)

OBJS   = $(addprefix $(BUILD)/,$(C_SRCS:.c=.o)) $(addprefix $(BUILD)/,$(ASM_SRCS:.asm=.o))
KERNEL = $(BUILD)/kernelab.bin

.PHONY: all run iso lint clean

all: $(KERNEL)

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/%.o: %.c $(HEADERS) | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/%.o: %.asm | $(BUILD)
	$(ASM) $(ASFLAGS) $< -o $@

$(KERNEL): $(OBJS) linker.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJS)

iso: $(KERNEL)
	mkdir -p $(ISODIR)/boot/grub
	cp $(KERNEL) $(ISODIR)/boot/kernelab.bin
	cp boot/grub.cfg $(ISODIR)/boot/grub/grub.cfg
	grub-mkrescue -o $(BUILD)/kernelab.iso $(ISODIR)

run: iso
	qemu-system-i386 -cdrom $(BUILD)/kernelab.iso

lint:
	python3 tools/lint.py

clean:
	rm -rf $(BUILD) $(ISODIR)
