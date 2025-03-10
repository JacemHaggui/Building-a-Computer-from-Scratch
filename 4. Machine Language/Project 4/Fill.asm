// Initialize screen address
@SCREEN
D=A
@addr
M=D             // addr = SCREEN (start address)

// Main loop
(LOOP)
    @KBD
    D=M         // D = key input

    @FILL
    D;JNE       // If key pressed, jump to FILL

    @CLEAR
    0;JMP       // Else, clear the screen

// Fill one word (black) and advance
(FILL)
    // Checking if we are at the edge
    @SCREEN
    D=A
    @addr
    D=M-D       // D = addr - SCREEN (how many words have passed)

    @8192
    D=D-A       // D = current offset - 8192

    @LOOP
    D;JGE       // If addr >= SCREEN + 8192, restart the loop

    // Filling the screen
    @addr
    A=M         // Access the pointer
    M=-1        // Set word to all 1s (black)

    @addr
    M=M+1       // addr++

    @LOOP
    0;JMP

// Clear one word (white) and advance
(CLEAR)

    // Checking if we are at the edge
    @SCREEN
    D=A
    @addr
    D=M-D       // D = addr - SCREEN (how many words have passed)

    @LOOP
    D;JLT       // If addr <= SCREEN, restart the loop

    // Emptying the screen
    @addr
    A=M
    M=0         // Set word to all 0s (white)

    @addr
    M=M-1       // addr--

// Back to main loop
@LOOP
0;JMP