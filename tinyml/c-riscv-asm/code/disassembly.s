
hello.o:     file format elf32-littleriscv


Disassembly of section .text:

00000000 <main>:
   0:	1101                	addi	sp,sp,-32
   2:	ce06                	sw	ra,28(sp)
   4:	cc22                	sw	s0,24(sp)
   6:	1000                	addi	s0,sp,32
   8:	444447b7          	lui	a5,0x44444
   c:	44478793          	addi	a5,a5,1092 # 44444444 <static_var.0+0x44444440>
  10:	fef42623          	sw	a5,-20(s0)
  14:	000007b7          	lui	a5,0x0
  18:	00078513          	mv	a0,a5
  1c:	00000097          	auipc	ra,0x0
  20:	000080e7          	jalr	ra # 1c <main+0x1c>
  24:	0001                	nop
  26:	40f2                	lw	ra,28(sp)
  28:	4462                	lw	s0,24(sp)
  2a:	6105                	addi	sp,sp,32
  2c:	8082                	ret
