/* Thanks compiler */

.section .text
.cc_top getChanend.elim, getChanend
.globl getChanend
.align 4
getChanend:
	getr r1,2
	bf r1,retGetChanend
	setd res[r1],r0
retGetChanend:
	mov r0,r1
	retsp 0
.cc_bottom getChanend.elim

.cc_top getLocalAnonChanend.elim, getLocalAnonChanend
.globl getLocalAnonChanend
.global getLocalAnonChanend.nstackwords
.linkset getLocalAnonChanend.nstackwords, 0
.align 4
getLocalAnonChanend:
	getr r0,0x2
	retsp 0x0
.cc_bottom getLocalAnonChanend.elim

.cc_top resetChans.elim, resetChans
.globl resetChans
.align 4
resetChans:
	entsp 0x1
getAllChans:
	stw r4,sp[0x0]
	getr r0,0x2
	bt r0,getAllChans
	ldc r2,0x1f
	ldc r3,0x1
	ldc r1,0x100
	ldc r0,0x2
	add r0,r0,r1
freeAllChans:
	freer res[r0]
	add r0,r0,r1
	eq r4,r3,r2
	add r3,r3,0x1
	bf r4,freeAllChans
	ldw r4,sp[0x0]
	retsp 0x1
.cc_bottom resetChans.elim

