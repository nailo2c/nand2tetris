// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// Idea
// a * b = a + a + ... + a
// for (i=0; i<b; i++) {
//     c = c + a
// }
// Pseudo Code
// a = RAM[0]
// b = RAM[1]
// c = RAM[2]
// i = 0
// LOOP:
//     if i >= b goto END
//     c = c + a
//     i = i + 1
//     goto LOOP
// END:
//     goto END

    @R0
    D=M // D=RAM(0)
    @a
    M=D // a=RAM(0)

    @R1
    D=M 
    @b
    M=D // b=RAM(1)

    @i
    M=0 // i=0

    @sum
    M=0

    // if a=0 or b=0, then set c=0 goto ZERO
    @za
    D=M
    @a
    D=D-M
    @ZERO
    D;JEQ

    @zb
    D=M
    @b
    D=D-M
    @ZERO
    D;JEQ

(LOOP)
    // if i - b >=0 goto END
    @i
    D=M // D=RAM(i)
    @b
    D=D-M // D=RAM(i)-RAM(b)
    @END
    D;JGE
    // else sum = sum + a ; i = i + 1
    @a
    D=M     // D = RAM(a)
    @sum
    M=D+M   // RAM(sum) = RAM(a) + RAM(sum)

    @i
    M=M+1   // RAM(i) = RAM(i) + 1

    @LOOP
    0;JMP

(END)
    @sum
    D=M // D = RAM(sum)
    @R2
    M=D // RAM(R2) = RAM(sum)
    @END
    0;JMP

(ZERO)
    @R2
    M=0
    @ZERO
    0;JMP
