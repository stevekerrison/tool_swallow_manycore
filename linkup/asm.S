/* Thanks compiler */

.section .text
.cc_top getChanend.elim, getChanend
.globl getChanend
.align 4
getChanend:
	getr r1,2
	setd res[r1],r0
	mov r0,r1
	retsp 0
.cc_bottom getChanend.elim
