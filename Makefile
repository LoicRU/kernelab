CC      = gcc
ASM     = nasm
LD      = ld
CFLAGS  = -m32 -ffreestanding -fno-pie -fno-stack-protector -nostdlib \
          -Wall -Wextra -std=gnu11 -Idrivers -Ikernel
ASFLAGS = -f elf32
LDFLAGS = -m elf_i386 -T linker.ld

BUILD = build
ISODIR = iso

OBJS = $(BUILD)/boot.o $(BUILD)/kernel.o $(BUILD)/vga.o
KERNEL = $(BUILD)/kernelab.bin

.PHONY: all run iso lint clean

all: $(KERNEL)

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/boot.o: boot/boot.asm | $(BUILD)
	$(ASM) $(ASFLAGS) $< -o $@

$(BUILD)/kernel.o: kernel/kernel.c drivers/vga.h | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/vga.o: drivers/vga.c drivers/vga.h | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

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
