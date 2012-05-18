          .file     "main.xc"
          .section .netinfo,       "", @netinfo
          .int      0x1eaba15c
.extern configure_in_port_handshake, "f{0}(w:p,i:p,o:p,ck)"
.extern configure_out_port_handshake, "f{0}(w:p,i:p,o:p,ck,ui)"
.extern configure_in_port_strobed_master, "f{0}(w:p,o:p,:ck)"
.extern configure_out_port_strobed_master, "f{0}(w:p,o:p,:ck,ui)"
.extern configure_in_port_strobed_slave, "f{0}(w:p,i:p,ck)"
.extern configure_out_port_strobed_slave, "f{0}(w:p,i:p,ck,ui)"
.extern configure_in_port, "f{0}(w:p,:ck)"
.extern configure_in_port_no_ready, "f{0}(w:p,:ck)"
.extern configure_out_port, "f{0}(w:p,:ck,ui)"
.extern configure_out_port_no_ready, "f{0}(w:p,:ck,ui)"
.extern configure_port_clock_output, "f{0}(w:p,:ck)"
.extern start_port, "f{0}(w:p)"
.extern stop_port, "f{0}(w:p)"
.extern configure_clock_src, "f{0}(ck,w:p)"
.extern configure_clock_ref, "f{0}(ck,uc)"
.extern configure_clock_rate, "f{0}(ck,ui,ui)"
.extern configure_clock_rate_at_least, "f{0}(ck,ui,ui)"
.extern configure_clock_rate_at_most, "f{0}(ck,ui,ui)"
.extern set_clock_src, "f{0}(ck,w:p)"
.extern set_clock_ref, "f{0}(ck)"
.extern set_clock_div, "f{0}(ck,uc)"
.extern set_clock_rise_delay, "f{0}(ck,ui)"
.extern set_clock_fall_delay, "f{0}(ck,ui)"
.extern set_port_clock, "f{0}(w:p,:ck)"
.extern set_port_ready_src, "f{0}(w:p,w:p)"
.extern set_clock_ready_src, "f{0}(ck,w:p)"
.extern set_clock_on, "f{0}(ck)"
.extern set_clock_off, "f{0}(ck)"
.extern start_clock, "f{0}(ck)"
.extern stop_clock, "f{0}(ck)"
.extern set_port_use_on, "f{0}(w:p)"
.extern set_port_use_off, "f{0}(w:p)"
.extern set_port_mode_data, "f{0}(w:p)"
.extern set_port_mode_clock, "f{0}(w:p)"
.extern set_port_mode_ready, "f{0}(w:p)"
.extern set_port_drive, "f{0}(w:p)"
.extern set_port_drive_low, "f{0}(w:p)"
.extern set_port_pull_up, "f{0}(w:p)"
.extern set_port_pull_down, "f{0}(w:p)"
.extern set_port_pull_none, "f{0}(w:p)"
.extern set_port_master, "f{0}(w:p)"
.extern set_port_slave, "f{0}(w:p)"
.extern set_port_no_ready, "f{0}(w:p)"
.extern set_port_strobed, "f{0}(w:p)"
.extern set_port_handshake, "f{0}(w:p)"
.extern set_port_no_sample_delay, "f{0}(w:p)"
.extern set_port_sample_delay, "f{0}(w:p)"
.extern set_port_no_inv, "f{0}(w:p)"
.extern set_port_inv, "f{0}(w:p)"
.extern set_port_shift_count, "f{0}(w:p,ui)"
.extern set_pad_delay, "f{0}(w:p,ui)"
.extern set_thread_fast_mode_on, "f{0}(0)"
.extern set_thread_fast_mode_off, "f{0}(0)"
.extern start_streaming_slave, "f{0}(chd)"
.extern start_streaming_master, "f{0}(chd)"
.extern stop_streaming_slave, "f{0}(chd)"
.extern stop_streaming_master, "f{0}(chd)"
.extern outuchar, "f{0}(chd,uc)"
.extern outuint, "f{0}(chd,ui)"
.extern inuchar, "f{uc}(chd)"
.extern inuint, "f{ui}(chd)"
.extern inuchar_byref, "f{0}(chd,&(uc))"
.extern inuint_byref, "f{0}(chd,&(ui))"
.extern sync, "f{0}(w:p)"
.extern peek, "f{ui}(w:p)"
.extern clearbuf, "f{0}(w:p)"
.extern endin, "f{ui}(w:p)"
.extern partin, "f{ui}(w:p,ui)"
.extern partout, "f{0}(w:p,ui,ui)"
.extern partout_timed, "f{ui}(w:p,ui,ui,ui)"
.extern partin_timestamped, "f{ui,ui}(w:p,ui)"
.extern partout_timestamped, "f{ui}(w:p,ui,ui)"
.extern outct, "f{0}(chd,uc)"
.extern chkct, "f{0}(chd,uc)"
.extern inct, "f{uc}(chd)"
.extern inct_byref, "f{0}(chd,&(uc))"
.extern testct, "f{si}(chd)"
.extern testwct, "f{si}(chd)"
.extern soutct, "f{0}(m:chd,uc)"
.extern schkct, "f{0}(m:chd,uc)"
.extern sinct, "f{uc}(m:chd)"
.extern sinct_byref, "f{0}(m:chd,&(uc))"
.extern stestct, "f{si}(m:chd)"
.extern stestwct, "f{si}(m:chd)"
.extern out_char_array, "ft{0}(chd,&(a(:c:uc)),ui)"
.extern in_char_array, "ft{0}(chd,&(a(:uc)),ui)"
.extern crc32, "f{0}(&(ui),ui,ui)"
.extern crc8shr, "f{ui}(&(ui),ui,ui)"
.extern lmul, "f{ui,ui}(ui,ui,ui,ui)"
.extern mac, "f{ui,ui}(ui,ui,ui,ui)"
.extern macs, "f{si,ui}(si,si,si,ui)"
.extern sext, "f{si}(ui,ui)"
.extern zext, "f{ui}(ui,ui)"
.extern pinseq, "f{0}(ui)"
.extern pinsneq, "f{0}(ui)"
.extern pinseq_at, "f{0}(ui,ui)"
.extern pinsneq_at, "f{0}(ui,ui)"
.extern timerafter, "f{0}(ui)"
.extern getps, "f{ui}(ui)"
.extern setps, "f{0}(ui,ui)"
.extern read_pswitch_reg, "f{si}(ui,ui,&(ui))"
.extern read_sswitch_reg, "f{si}(ui,ui,&(ui))"
.extern write_pswitch_reg, "f{si}(ui,ui,ui)"
.extern write_pswitch_reg_no_ack, "f{si}(ui,ui,ui)"
.extern write_sswitch_reg, "f{si}(ui,ui,ui)"
.extern write_sswitch_reg_no_ack, "f{si}(ui,ui,ui)"
.extern read_node_config_reg, "f{si}(cr,ui,&(ui))"
.extern write_node_config_reg, "f{si}(cr,ui,ui)"
.extern write_node_config_reg_no_ack, "f{si}(cr,ui,ui)"
.extern read_periph_8, "f{si}(cr,ui,ui,ui,&(a(:uc)))"
.extern write_periph_8, "f{si}(cr,ui,ui,ui,&(a(:c:uc)))"
.extern write_periph_8_no_ack, "f{si}(cr,ui,ui,ui,&(a(:c:uc)))"
.extern read_periph_32, "f{si}(cr,ui,ui,ui,&(a(:ui)))"
.extern write_periph_32, "f{si}(cr,ui,ui,ui,&(a(:c:ui)))"
.extern write_periph_32_no_ack, "f{si}(cr,ui,ui,ui,&(a(:c:ui)))"
.extern get_core_id, "f{ui}(0)"
.extern get_thread_id, "f{ui}(0)"
.extern __builtin_getid, "f{si}(0)"
.extern printf, "f{si}(&(a(:c:uc)),va)"
.extern scanf, "f{si}(&(a(:c:uc)),va)"
.extern sscanf, "f{si}(&(a(:c:uc)),&(a(:c:uc)),va)"
.extern getchar, "f{si}(0)"
.extern putchar, "f{si}(si)"
.extern puts, "f{si}(&(a(:c:uc)))"
.extern perror, "f{0}(&(a(:c:uc)))"
.extern sprintf, "f{si}(&(a(:uc)),&(a(:c:uc)),va)"
.extern remove, "f{si}(&(a(:c:uc)))"
.extern rename, "f{si}(&(a(:c:uc)),&(a(:c:uc)))"
.extern diprintf, "f{si}(si,&(a(:c:uc)),va)"
.extern fcloseall, "f{si}(0)"
.extern iprintf, "f{si}(&(a(:c:uc)),va)"
.extern iscanf, "f{si}(&(a(:c:uc)),va)"
.extern siprintf, "f{si}(&(a(:uc)),&(a(:c:uc)),va)"
.extern siscanf, "f{si}(&(a(:c:uc)),&(a(:c:uc)),va)"
.extern snprintf, "f{si}(&(a(:uc)),ui,&(a(:c:uc)),va)"
.extern sniprintf, "f{si}(&(a(:uc)),ui,&(a(:c:uc)),va)"
.extern c0, "f{0}(chd)"
.extern c1, "f{0}(chd)"
main.parinfo.debugstring0:
.asciiz "# 8 \"main.xc\""
main.parinfo.debugstring1:
.asciiz "# 6 \"main.xc\""
.cc_top main.parinfo.cc, main.parinfo
.globl main.parinfo, "pi"
.type  main.parinfo, @object
main.parinfo:
          .int      0x00000004
          .long __main_default_network
          .long main.parinfo.debugstring0
          .long main.parinfo.debugstring1
          .int      0x00000008
          .int      0x00000000
          .int      $N __main_xm_0
          .long stdcore
          .int      0x00000001
          .int      0x00000000
          .int      $N __main_xm_1
          .long stdcore + 4
          .int      0x00000001
          .int      0x00000000
          .int      $N __main_xm_2
          .long stdcore + 8
          .int      0x00000001
          .int      0x00000001
          .int      $N __main_xm_3
          .long stdcore + 12
          .int      0x00000001
          .int      0x00000001
          .int      $N __main_xm_4
          .long stdcore + 16
          .int      0x00000001
          .int      0x00000002
          .int      $N __main_xm_5
          .long stdcore + 20
          .int      0x00000001
          .int      0x00000002
          .int      $N __main_xm_6
          .long stdcore + 24
          .int      0x00000001
          .int      0x00000003
          .int      $N __main_xm_7
          .long stdcore + 28
          .int      0x00000001
          .int      0x00000003
.cc_bottom main.parinfo.cc
          .text
          .align    2
.cc_top __main_xm_7.function,__main_xm_7
          .align    4
.call __main_xm_7, c1
.globl __main_xm_7, "f{0}(chd)"
.globl __main_xm_7.nstackwords
.globl __main_xm_7.maxthreads
.globl __main_xm_7.maxtimers
.globl __main_xm_7.maxchanends
.globl __main_xm_7.maxsync
.type  __main_xm_7, @function
.linkset __main_xm_7.locnoside, 1
.linkset __main_xm_7.locnochandec, 1
.linkset .LLNK1, c1.nstackwords $M c1.nstackwords
.linkset .LLNK0, .LLNK1 + 10
.linkset __main_xm_7.nstackwords, .LLNK0
__main_xm_7:
          entsp     0xa 
          stw       r0, sp[0x1] 
          ldaw      r1, sp[0x2] 
          ldw       r0, sp[0x1] 
          stw       r0, r1[0x6] 
.L2:
          ldaw      r0, sp[0x2] 
          ldw       r0, r0[0x6] 
.L4:
          bl        c1 
.L1:
.L3:
          retsp     0xa 
.size __main_xm_7, .-__main_xm_7
.cc_bottom __main_xm_7.function
.linkset __main_xm_7.maxchanends, c1.maxchanends
.linkset __main_xm_7.maxtimers, c1.maxtimers
.linkset .LLNK4, c1.maxthreads - 1
.linkset .LLNK3, 1 + .LLNK4
.linkset .LLNK2, 1 $M .LLNK3
.linkset __main_xm_7.maxthreads, .LLNK2
.cc_top __main_xm_6.function,__main_xm_6
          .align    4
.call __main_xm_6, c0
.globl __main_xm_6, "f{0}(chd)"
.globl __main_xm_6.nstackwords
.globl __main_xm_6.maxthreads
.globl __main_xm_6.maxtimers
.globl __main_xm_6.maxchanends
.globl __main_xm_6.maxsync
.type  __main_xm_6, @function
.linkset __main_xm_6.locnoside, 1
.linkset __main_xm_6.locnochandec, 1
.linkset .LLNK6, c0.nstackwords $M c0.nstackwords
.linkset .LLNK5, .LLNK6 + 10
.linkset __main_xm_6.nstackwords, .LLNK5
__main_xm_6:
          entsp     0xa 
          stw       r0, sp[0x1] 
          ldaw      r1, sp[0x2] 
          ldw       r0, sp[0x1] 
          stw       r0, r1[0x6] 
.L7:
          ldaw      r0, sp[0x2] 
          ldw       r0, r0[0x6] 
.L9:
          bl        c0 
.L6:
.L8:
          retsp     0xa 
.size __main_xm_6, .-__main_xm_6
.cc_bottom __main_xm_6.function
.linkset __main_xm_6.maxchanends, c0.maxchanends
.linkset __main_xm_6.maxtimers, c0.maxtimers
.linkset .LLNK9, c0.maxthreads - 1
.linkset .LLNK8, 1 + .LLNK9
.linkset .LLNK7, 1 $M .LLNK8
.linkset __main_xm_6.maxthreads, .LLNK7
.cc_top __main_xm_5.function,__main_xm_5
          .align    4
.call __main_xm_5, c1
.globl __main_xm_5, "f{0}(chd)"
.globl __main_xm_5.nstackwords
.globl __main_xm_5.maxthreads
.globl __main_xm_5.maxtimers
.globl __main_xm_5.maxchanends
.globl __main_xm_5.maxsync
.type  __main_xm_5, @function
.linkset __main_xm_5.locnoside, 1
.linkset __main_xm_5.locnochandec, 1
.linkset .LLNK11, c1.nstackwords $M c1.nstackwords
.linkset .LLNK10, .LLNK11 + 10
.linkset __main_xm_5.nstackwords, .LLNK10
__main_xm_5:
          entsp     0xa 
          stw       r0, sp[0x1] 
          ldaw      r1, sp[0x2] 
          ldw       r0, sp[0x1] 
          stw       r0, r1[0x4] 
.L12:
          ldaw      r0, sp[0x2] 
          ldw       r0, r0[0x4] 
.L14:
          bl        c1 
.L11:
.L13:
          retsp     0xa 
.size __main_xm_5, .-__main_xm_5
.cc_bottom __main_xm_5.function
.linkset __main_xm_5.maxchanends, c1.maxchanends
.linkset __main_xm_5.maxtimers, c1.maxtimers
.linkset .LLNK14, c1.maxthreads - 1
.linkset .LLNK13, 1 + .LLNK14
.linkset .LLNK12, 1 $M .LLNK13
.linkset __main_xm_5.maxthreads, .LLNK12
.cc_top __main_xm_4.function,__main_xm_4
          .align    4
.call __main_xm_4, c0
.globl __main_xm_4, "f{0}(chd)"
.globl __main_xm_4.nstackwords
.globl __main_xm_4.maxthreads
.globl __main_xm_4.maxtimers
.globl __main_xm_4.maxchanends
.globl __main_xm_4.maxsync
.type  __main_xm_4, @function
.linkset __main_xm_4.locnoside, 1
.linkset __main_xm_4.locnochandec, 1
.linkset .LLNK16, c0.nstackwords $M c0.nstackwords
.linkset .LLNK15, .LLNK16 + 10
.linkset __main_xm_4.nstackwords, .LLNK15
__main_xm_4:
          entsp     0xa 
          stw       r0, sp[0x1] 
          ldaw      r1, sp[0x2] 
          ldw       r0, sp[0x1] 
          stw       r0, r1[0x4] 
.L17:
          ldaw      r0, sp[0x2] 
          ldw       r0, r0[0x4] 
.L19:
          bl        c0 
.L16:
.L18:
          retsp     0xa 
.size __main_xm_4, .-__main_xm_4
.cc_bottom __main_xm_4.function
.linkset __main_xm_4.maxchanends, c0.maxchanends
.linkset __main_xm_4.maxtimers, c0.maxtimers
.linkset .LLNK19, c0.maxthreads - 1
.linkset .LLNK18, 1 + .LLNK19
.linkset .LLNK17, 1 $M .LLNK18
.linkset __main_xm_4.maxthreads, .LLNK17
.cc_top __main_xm_3.function,__main_xm_3
          .align    4
.call __main_xm_3, c1
.globl __main_xm_3, "f{0}(chd)"
.globl __main_xm_3.nstackwords
.globl __main_xm_3.maxthreads
.globl __main_xm_3.maxtimers
.globl __main_xm_3.maxchanends
.globl __main_xm_3.maxsync
.type  __main_xm_3, @function
.linkset __main_xm_3.locnoside, 1
.linkset __main_xm_3.locnochandec, 1
.linkset .LLNK21, c1.nstackwords $M c1.nstackwords
.linkset .LLNK20, .LLNK21 + 10
.linkset __main_xm_3.nstackwords, .LLNK20
__main_xm_3:
          entsp     0xa 
          stw       r0, sp[0x1] 
          ldaw      r1, sp[0x2] 
          ldw       r0, sp[0x1] 
          stw       r0, r1[0x2] 
.L22:
          ldaw      r0, sp[0x2] 
          ldw       r0, r0[0x2] 
.L24:
          bl        c1 
.L21:
.L23:
          retsp     0xa 
.size __main_xm_3, .-__main_xm_3
.cc_bottom __main_xm_3.function
.linkset __main_xm_3.maxchanends, c1.maxchanends
.linkset __main_xm_3.maxtimers, c1.maxtimers
.linkset .LLNK24, c1.maxthreads - 1
.linkset .LLNK23, 1 + .LLNK24
.linkset .LLNK22, 1 $M .LLNK23
.linkset __main_xm_3.maxthreads, .LLNK22
.cc_top __main_xm_2.function,__main_xm_2
          .align    4
.call __main_xm_2, c0
.globl __main_xm_2, "f{0}(chd)"
.globl __main_xm_2.nstackwords
.globl __main_xm_2.maxthreads
.globl __main_xm_2.maxtimers
.globl __main_xm_2.maxchanends
.globl __main_xm_2.maxsync
.type  __main_xm_2, @function
.linkset __main_xm_2.locnoside, 1
.linkset __main_xm_2.locnochandec, 1
.linkset .LLNK26, c0.nstackwords $M c0.nstackwords
.linkset .LLNK25, .LLNK26 + 10
.linkset __main_xm_2.nstackwords, .LLNK25
__main_xm_2:
          entsp     0xa 
          stw       r0, sp[0x1] 
          ldaw      r1, sp[0x2] 
          ldw       r0, sp[0x1] 
          stw       r0, r1[0x2] 
.L27:
          ldaw      r0, sp[0x2] 
          ldw       r0, r0[0x2] 
.L29:
          bl        c0 
.L26:
.L28:
          retsp     0xa 
.size __main_xm_2, .-__main_xm_2
.cc_bottom __main_xm_2.function
.linkset __main_xm_2.maxchanends, c0.maxchanends
.linkset __main_xm_2.maxtimers, c0.maxtimers
.linkset .LLNK29, c0.maxthreads - 1
.linkset .LLNK28, 1 + .LLNK29
.linkset .LLNK27, 1 $M .LLNK28
.linkset __main_xm_2.maxthreads, .LLNK27
.cc_top __main_xm_1.function,__main_xm_1
          .align    4
.call __main_xm_1, c1
.globl __main_xm_1, "f{0}(chd)"
.globl __main_xm_1.nstackwords
.globl __main_xm_1.maxthreads
.globl __main_xm_1.maxtimers
.globl __main_xm_1.maxchanends
.globl __main_xm_1.maxsync
.type  __main_xm_1, @function
.linkset __main_xm_1.locnoside, 1
.linkset __main_xm_1.locnochandec, 1
.linkset .LLNK31, c1.nstackwords $M c1.nstackwords
.linkset .LLNK30, .LLNK31 + 10
.linkset __main_xm_1.nstackwords, .LLNK30
__main_xm_1:
          entsp     0xa 
          stw       r0, sp[0x1] 
          ldaw      r1, sp[0x2] 
          ldw       r0, sp[0x1] 
          stw       r0, r1[0x0] 
.L32:
          ldaw      r0, sp[0x2] 
          ldw       r0, r0[0x0] 
.L34:
          bl        c1 
.L31:
.L33:
          retsp     0xa 
.size __main_xm_1, .-__main_xm_1
.cc_bottom __main_xm_1.function
.linkset __main_xm_1.maxchanends, c1.maxchanends
.linkset __main_xm_1.maxtimers, c1.maxtimers
.linkset .LLNK34, c1.maxthreads - 1
.linkset .LLNK33, 1 + .LLNK34
.linkset .LLNK32, 1 $M .LLNK33
.linkset __main_xm_1.maxthreads, .LLNK32
.cc_top __main_xm_0.function,__main_xm_0
          .align    4
.call __main_xm_0, c0
.globl __main_xm_0, "f{0}(chd)"
.globl __main_xm_0.nstackwords
.globl __main_xm_0.maxthreads
.globl __main_xm_0.maxtimers
.globl __main_xm_0.maxchanends
.globl __main_xm_0.maxsync
.type  __main_xm_0, @function
.linkset __main_xm_0.locnoside, 1
.linkset __main_xm_0.locnochandec, 1
.linkset .LLNK36, c0.nstackwords $M c0.nstackwords
.linkset .LLNK35, .LLNK36 + 10
.linkset __main_xm_0.nstackwords, .LLNK35
__main_xm_0:
          entsp     0xa 
          stw       r0, sp[0x1] 
          ldaw      r1, sp[0x2] 
          ldw       r0, sp[0x1] 
          stw       r0, r1[0x0] 
.L37:
          ldaw      r0, sp[0x2] 
          ldw       r0, r0[0x0] 
.L39:
          bl        c0 
.L36:
.L38:
          retsp     0xa 
.size __main_xm_0, .-__main_xm_0
.cc_bottom __main_xm_0.function
.linkset __main_xm_0.maxchanends, c0.maxchanends
.linkset __main_xm_0.maxtimers, c0.maxtimers
.linkset .LLNK39, c0.maxthreads - 1
.linkset .LLNK38, 1 + .LLNK39
.linkset .LLNK37, 1 $M .LLNK38
.linkset __main_xm_0.maxthreads, .LLNK37
.par c1, c0, "main.xc:8: error: use of `%s' violates parallel usage rules"
.par c1, c1, "main.xc:8: error: use of `%s' violates parallel usage rules"
.par c0, c0, "main.xc:8: error: use of `%s' violates parallel usage rules"
# Thread names for recovering thread graph in linker
.set thread.anon.8, 0  #unreal
.set thread.anon.9, 0  #unreal
.set thread.anon.19, 0  #unreal
.set thread.anon.24, 0  #unreal
.set thread.anon.15, 0  #unreal
.set thread.anon.16, 0  #unreal
.set thread.anon.13, 0  #unreal
.set thread.anon.21, 0  #unreal
.set thread.anon.22, 0  #unreal
.set thread.anon.23, 0  #unreal
.set thread.anon.0, 0  #unreal
.set thread.anon.17, 0  #unreal
.set thread.anon.18, 0  #unreal
.set thread.anon.1, 0  #unreal
.set thread.anon.2, 0  #unreal
.set thread.anon.3, 0  #unreal
.set thread.anon.4, 0  #unreal
.set thread.anon.6, 0  #unreal
.set thread.anon.14, 0  #unreal
.set thread.anon.10, 0  #unreal
.set thread.anon.12, 0  #unreal
.set thread.anon.5, 0  #unreal
.set thread.anon.7, 0  #unreal
.set thread.anon.11, 0  #unreal
.set thread.anon.20, 0  #unreal
.extern __builtin_getid, "f{si}(0)"
.extern stdcore, "a(2147483647:cr)"
.extern __builtin_getid, "f{si}(0)"
          .section .xtalabeltable,       "", @progbits
.L40:
          .int      .L41-.L40
          .int      0x00000000
          .asciiz   "/home/steve/phd/sandbox/xmp16/linkup"
.cc_top __main_xm_0.function, __main_xm_0
          .asciiz  "main.xc"
          .int      0x0000000e
          .int      0x0000000e
# line info for line 14 
          .long    .L38
          .asciiz  "main.xc"
          .int      0x0000000a
          .int      0x0000000a
# line info for line 10 
          .long    .L37
.cc_bottom __main_xm_0.function
.cc_top __main_xm_1.function, __main_xm_1
          .asciiz  "main.xc"
          .int      0x0000000e
          .int      0x0000000e
# line info for line 14 
          .long    .L33
          .asciiz  "main.xc"
          .int      0x0000000b
          .int      0x0000000b
# line info for line 11 
          .long    .L32
.cc_bottom __main_xm_1.function
.cc_top __main_xm_2.function, __main_xm_2
          .asciiz  "main.xc"
          .int      0x0000000e
          .int      0x0000000e
# line info for line 14 
          .long    .L28
          .asciiz  "main.xc"
          .int      0x0000000a
          .int      0x0000000a
# line info for line 10 
          .long    .L27
.cc_bottom __main_xm_2.function
.cc_top __main_xm_3.function, __main_xm_3
          .asciiz  "main.xc"
          .int      0x0000000e
          .int      0x0000000e
# line info for line 14 
          .long    .L23
          .asciiz  "main.xc"
          .int      0x0000000b
          .int      0x0000000b
# line info for line 11 
          .long    .L22
.cc_bottom __main_xm_3.function
.cc_top __main_xm_4.function, __main_xm_4
          .asciiz  "main.xc"
          .int      0x0000000e
          .int      0x0000000e
# line info for line 14 
          .long    .L18
          .asciiz  "main.xc"
          .int      0x0000000a
          .int      0x0000000a
# line info for line 10 
          .long    .L17
.cc_bottom __main_xm_4.function
.cc_top __main_xm_5.function, __main_xm_5
          .asciiz  "main.xc"
          .int      0x0000000e
          .int      0x0000000e
# line info for line 14 
          .long    .L13
          .asciiz  "main.xc"
          .int      0x0000000b
          .int      0x0000000b
# line info for line 11 
          .long    .L12
.cc_bottom __main_xm_5.function
.cc_top __main_xm_6.function, __main_xm_6
          .asciiz  "main.xc"
          .int      0x0000000e
          .int      0x0000000e
# line info for line 14 
          .long    .L8
          .asciiz  "main.xc"
          .int      0x0000000a
          .int      0x0000000a
# line info for line 10 
          .long    .L7
.cc_bottom __main_xm_6.function
.cc_top __main_xm_7.function, __main_xm_7
          .asciiz  "main.xc"
          .int      0x0000000e
          .int      0x0000000e
# line info for line 14 
          .long    .L3
          .asciiz  "main.xc"
          .int      0x0000000b
          .int      0x0000000b
# line info for line 11 
          .long    .L2
.cc_bottom __main_xm_7.function
.L41:
          .section .dp.data,       "adw", @progbits
.align 4
          .align    4
          .section .dp.bss,        "adw", @nobits
.align 4
          .ident    "XMOS 32-bit XC Compiler 11.11.0 (build 2237)"
          .core     "XS1"
          .corerev  "REVB"
