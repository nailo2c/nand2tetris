// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// Pseudo Code
// LOOP:
//     if KEB==0 goto END
//     blacken
//     goto LOOP
// END:
//     whiten
//     goto LOOP
(LOOP)
    @KBD  // 24576
    D=M   // D=RAM(KBD)=RAM(24576), e.g. D=100 if input='d' 
    @END
    D;JEQ // Jump to END if no input (i.e. D=0)

    // store screen and keyboard address
    @SCREEN
    D=A     // D=16384
    @scaddr
    M=D     // M=RAM(addr)=16384 (i.e. RAM(16)=16384)
    @KBD
    D=A     // D=24576
    @kbaddr
    M=D     // M=RAM(kbaddr)=24576 (i.e. RAM(17)=24576

    // blacken
    (LOOP2)
        @scaddr
        A=M // A=RAM(16384)
        M=-1 // RAM(16384)=-1
        @scaddr
        M=M+1 // addr=addr+1
        D=M   // D=RAM(addr)=RAM(16)
        @kbaddr
        D=D-M // D=RAM(16)-24576
        @LOOP
        D;JEQ
        @LOOP2
        0;JMP

    @LOOP
    0;JMP
(END)
    // store screen and keyboard address
    @SCREEN
    D=A     // D=16384
    @scaddr
    M=D     // M=RAM(addr)=16384 (i.e. RAM(16)=16384)
    @KBD
    D=A     // D=24576
    @kbaddr
    M=D     // M=RAM(kbaddr)=24576 (i.e. RAM(17)=24576
    // whiten
    (LOOP3)
        @scaddr
        A=M // A=RAM(16)=16384 (we need to get address of screen, o.w., M=0 would assign 0 to address 16)
        M=0 // RAM(16384)=0
        @scaddr
        M=M+1 // RAM(16)=16384+1
        D=M   // D=RAM(addr)=RAM(16)
        @kbaddr
        D=D-M // D=RAM(16)-24576
        @LOOP
        D;JEQ
        @LOOP3
        0;JMP

    @LOOP
    0;JMP
