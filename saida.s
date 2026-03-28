    .syntax unified
    .arch armv7-a
    .fpu vfpv3-d16

    .data
VAR_MEM: .space 8
RES_LINHA_1: .space 8
RES_LINHA_2: .space 8
RES_LINHA_3: .space 8
RES_LINHA_4: .space 8
RES_LINHA_5: .space 8
RES_LINHA_6: .space 8
RES_LINHA_7: .space 8
RES_LINHA_8: .space 8
RES_LINHA_9: .space 8
RES_LINHA_10: .space 8
RES_LINHA_11: .space 8
RES_LINHA_12: .space 8
CONST_1: .word 0x00000000, 0x40240000 @ valor: 10.0
CONST_2: .word 0x00000000, 0x40040000 @ valor: 2.5
CONST_3: .word 0x00000000, 0x401C0000 @ valor: 7.0
CONST_4: .word 0x00000000, 0x40080000 @ valor: 3.0
CONST_5: .word 0x00000000, 0x40000000 @ valor: 2.0
CONST_8: .word 0x00000000, 0x3FF00000 @ valor: 1.0
CONST_9: .word 0x00000000, 0x40140000 @ valor: 5.0
CONST_10: .word 0x00000000, 0x40100000 @ valor: 4.0
CONST_11: .word 0x00000000, 0x40220000 @ valor: 9.0
CONST_12: .word 0x00000000, 0x40490000 @ valor: 50.0

    .text
                                             
  @ UART_PUTCHAR - envia r0 (1 byte) por UART                                          
  UART_PUTCHAR:                                                                                     
      PUSH {r1, r2, lr}                                                                             
      LDR r2, =0xFF201000                                                                           
  _UART_WAIT:                                                                                     
      LDR r1, [r2, #4]        
      LSR r1, r1, #16                                                 
      CMP r1, #0                                                                                    
      BEQ _UART_WAIT                                                           
      STRB r0, [r2]                                                                 
      POP {r1, r2, pc}                                                                              
                                                                                                      
  @ PRINT_NIBBLES_32 - imprime r7 como 8 digitos hex
  PRINT_NIBBLES_32:                                                                                 
      PUSH {r6, r7, lr}                                                                             
      MOV r6, #8                                                   
  _LOOP_NIB:                                                                                        
      MOV r0, r7, LSR #28     
      AND r0, r0, #0xF                                                                              
      CMP r0, #10                                                                                 
      ADDLT r0, r0, #48       @ 0–9 :'0' = 48                                                    
      ADDGE r0, r0, #55       @ A–F :'A'–10 = 55                                                 
      BL UART_PUTCHAR
      LSL r7, r7, #4                                                             
      SUBS r6, r6, #1                                                                             
      BNE _LOOP_NIB                                                                                 
      POP {r6, r7, pc}                                                                            
                                                                                                                                                                                                      
  @ PRINT_RES_HEX - imprime double de 64 bits em hex
  @ r0 = endereco do valor                                                   
  PRINT_RES_HEX:                                                                                    
      PUSH {r4, r5, lr}                                                                             
      LDR r4, [r0]            @ word baixo                             
      LDR r5, [r0, #4]        @ word alto                                         
                                                                                                    
      MOV r0, #48             @ '0'                                                                 
      BL UART_PUTCHAR                                                                               
      MOV r0, #120            @ 'x'                                                               
      BL UART_PUTCHAR
                                                                                                    
      MOV r7, r5              @ word alto primeiro 
      BL PRINT_NIBBLES_32                                                                           
      MOV r7, r4              @ word baixo                                               
      BL PRINT_NIBBLES_32                                                                           
  
      MOV r0, #13             @ r                                                                
      BL UART_PUTCHAR                                                                             
      MOV r0, #10             @ n 
      BL UART_PUTCHAR                                                                               
  
      POP {r4, r5, pc}                                                                              
                        
    .global _start
_start:
    MRC p15, 0, r1, c1, c0, 2
    ORR r1, r1, #(0xF << 20)
    MCR p15, 0, r1, c1, c0, 2
    MOV r1, #0x40000000
    FMXR FPEXC, r1

    @ --- linha 1 ---
    LDR r0, =CONST_1
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_2
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VDIV.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_1
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_1
    BL PRINT_RES_HEX

    @ --- linha 2 ---
    LDR r0, =CONST_3
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_4
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VDIV.F64 d2, d0, d1
    VCVT.S32.F64 s4, d2
    VCVT.F64.S32 d2, s4
    VMUL.F64 d2, d2, d1
    VSUB.F64 d0, d0, d2
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_2
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_2
    BL PRINT_RES_HEX

    @ --- linha 3 ---
    LDR r0, =CONST_5
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_4
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VMOV.F64 d2, d0
    VCVT.S32.F64 s0, d1
    VMOV r2, s0
    LDR r0, =CONST_8
    VLDR d0, [r0]
POW_LOOP_6:
    CMP r2, #0
    BLE POW_FIM_7
    VMUL.F64 d0, d0, d2
    SUB r2, r2, #1
    B POW_LOOP_6
POW_FIM_7:
    VSTMDB sp!, {d0}
    LDR r0, =CONST_9
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_8
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VSUB.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VADD.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_3
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_3
    BL PRINT_RES_HEX

    @ --- linha 4 ---
    LDR r0, =CONST_8
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    ADD sp, sp, #8
    LDR r0, =RES_LINHA_3
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_5
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    ADD sp, sp, #8
    LDR r0, =RES_LINHA_2
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VMUL.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_4
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_4
    BL PRINT_RES_HEX

    @ --- linha 5 ---
    LDR r0, =CONST_10
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_11
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VMUL.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    LDR r0, =CONST_3
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_4
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VDIV.F64 d2, d0, d1
    VCVT.S32.F64 s4, d2
    VCVT.F64.S32 d0, s4
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VSUB.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_5
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_5
    BL PRINT_RES_HEX

    @ --- linha 6 ---
    LDR r0, =CONST_1
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_5
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VADD.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    LDR r0, =CONST_4
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_4
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VMUL.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VDIV.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_6
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_6
    BL PRINT_RES_HEX

    @ --- linha 7 ---
    LDR r0, =CONST_4
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    ADD sp, sp, #8
    LDR r0, =RES_LINHA_4
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_10
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    ADD sp, sp, #8
    LDR r0, =RES_LINHA_3
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VADD.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_7
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_7
    BL PRINT_RES_HEX

    @ --- linha 8 ---
    LDR r0, =CONST_12
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r1, =VAR_MEM
    VSTR d0, [r1]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_8
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_8
    BL PRINT_RES_HEX

    @ --- linha 9 ---
    LDR r0, =VAR_MEM
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_9
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VMUL.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_9
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_9
    BL PRINT_RES_HEX

    @ --- linha 10 ---
    LDR r0, =VAR_MEM
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_8
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    ADD sp, sp, #8
    LDR r0, =RES_LINHA_9
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VSUB.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_10
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_10
    BL PRINT_RES_HEX

    @ --- linha 11 ---
    LDR r0, =CONST_5
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_4
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_10
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VMUL.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VMUL.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    LDR r0, =CONST_9
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_2
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VDIV.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VADD.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_11
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_11
    BL PRINT_RES_HEX

    @ --- linha 12 ---
    LDR r0, =VAR_MEM
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    LDR r0, =CONST_5
    VLDR d0, [r0]
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d1}
    VLDMIA sp!, {d0}
    VADD.F64 d0, d0, d1
    VSTMDB sp!, {d0}
    VLDMIA sp!, {d0}
    LDR r3, =RES_LINHA_12
    VSTR d0, [r3]
    LDR r0, =RES_LINHA_12
    BL PRINT_RES_HEX

_end:
    B _end