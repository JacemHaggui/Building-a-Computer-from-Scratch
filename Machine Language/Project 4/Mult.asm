// i = 1
@i
M=1
// mult = 0
@mult
M=0

(LOOP)
// if (i > R0) goto STOP
@i
D=M
@R0
D=D-M
@STOP
D;JGT
// mult = mult + R1
@mult
D=M
@R1
D=D+M
@mult
M=D
// i = i + 1
@i
M=M+1
// goto LOOP
@LOOP
0;JMP

(STOP)
// R1 = sum
@mult
D=M
@R2
M=D
// infinite loop
(END)
@END
0;JMP