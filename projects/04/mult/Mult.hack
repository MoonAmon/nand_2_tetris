// Program: Mult.asm
// Do simple mult math RAM[2] = RAM[0] * RAM[1]
//

@R0
D=M
@factor1
M=D     // factor1 = RAM[0]
@R1
D=M
@n
M=D     // n = RAM[1]
@sum
M=0
@i
M=0     // initialize i = 0

(LOOP)
    @i
    D=M
    @n
    D=D-M
    @STOP
    D;JEQ // if i > n goto END

    @factor1
    D=M
    @sum
    M=D+M   // sum = sum + factor1
    @i
    M=M+1   // i = i + 1
    @LOOP
    0;JMP

(STOP)
    @sum
    D=M
    @R2
    M=D     // RAM[2] = sum


(END)
    @END
    0;JMP



