import conversion as cv
import os

symbol_table = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4
}

comp_table = {
    "0":   "0101010", "1":   "0111111", "-1":  "0111010",
    "D":   "0001100", "A":   "0110000", "!D":  "0001101",
    "!A":  "0110001", "-D":  "0001111", "-A":  "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M":   "1110000", "!M":  "1110001", "-M":  "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101"
}

dest_table = {
    None:  "000", "M":   "001", "D":   "010", "MD":  "011",
    "A":   "100", "AM":  "101", "AD":  "110", "AMD": "111"
}

jump_table = {
    None:  "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

try:
    # Get the file path and name from the user
    asmFile_path = "/Users/jacemhagui/Desktop/Academia/Coursera/NAND2TETRIS/Building-a-Computer-from-Scratch/6. Assembler/Project 6/Assembler/"
    file_name = input("Enter the name of the file you want to assemble (without .asm extension): ")
    asmFile = os.path.join(asmFile_path, file_name + ".asm")

    # Open and read the assembly file
    with open(asmFile, "r") as f:
        asmCode = f.read()
    
    # Open output file
    output_file = file_name + ".hack"
    log_file = "conversion_log.txt"
    
    with open(output_file, "w") as file, open(log_file, "w") as log:
        labels = {}  # Store label positions
        line_number = 0  # Track actual instruction lines
        cleaned_asm_code = []

        # First pass: Handle labels (L-instructions)
        print("First pass: Processing labels...")
        for line in asmCode.splitlines():
            AsmLine = line.strip()

            if AsmLine == "" or AsmLine.startswith("//"):
                continue

            # Handle labels (L-instructions)
            if AsmLine.startswith("(") and AsmLine.endswith(")"):
                label_name = AsmLine[1:-1]  # Remove parentheses
                labels[label_name] = line_number
                continue  # Labels don't count as real instructions

            cleaned_asm_code.append(line)  # Keep non-label and non-comment lines
            line_number += 1  # Only increment for actual instructions

        # Join cleaned lines back into a single string
        asmCode = "\n".join(cleaned_asm_code)
        
        # Second pass: Convert to binary
        print("\nSecond pass: Converting to binary...")
        line_number = 0  # Reset for second pass
        variable_pos = 16  # Start variable address assignment

        for line in asmCode.splitlines():
            AsmLine = line.strip()

            if AsmLine == "" or AsmLine.startswith("//"):
                continue

            print(f"\nProcessing line {line_number}: {AsmLine}")
            MachineLanguage = ['0'] * 16  # Default machine code

            # Handle A-instructions
            if AsmLine.startswith("@"):
                address = AsmLine[1:]

                # Check if it's a number or a label
                if address.isdigit():
                    binary_address = cv.decimal_to_binary(int(address), 15)
                    log.write(f"Line {line_number + 1}: A-instruction (numeric): @{address} -> {binary_address}\n")
                elif address in symbol_table:
                    binary_address = cv.decimal_to_binary(symbol_table.get(address, 0), 15)
                    log.write(f"Line {line_number + 1}: A-instruction (register): @{address} -> {binary_address}\n")
                elif address in labels:
                    binary_address = cv.decimal_to_binary(labels.get(address, 0), 15)
                    log.write(f"Line {line_number + 1}: A-instruction (label): @{address} -> {binary_address}\n")
                else:
                    # Declaring a new variable
                    binary_address = cv.decimal_to_binary(variable_pos, 15)
                    labels[address] = variable_pos
                    log.write(f"Line {line_number + 1}: Variable declared: @{address} -> {binary_address} at position {variable_pos}\n")
                    variable_pos += 1

                MachineLanguage[1:] = list(binary_address)  # Store binary address

            # Handle C-instructions
            else:
                log.write(f"Line {line_number + 1}: C-instruction: {AsmLine}\n")
                MachineLanguage[0:3] = "111"  # C-instruction prefix

                # Parse dest, comp, jump
                if "=" in AsmLine and ";" in AsmLine:
                    dest, rest = AsmLine.split("=")
                    comp, jump = rest.split(";")
                elif "=" in AsmLine:
                    dest, comp = AsmLine.split("=")
                    jump = None
                elif ";" in AsmLine:
                    dest = None
                    comp, jump = AsmLine.split(";")
                else:
                    dest, comp, jump = None, AsmLine, None

                log.write(f"  dest: {dest}, comp: {comp}, jump: {jump}\n")

                # Convert to binary using lookup tables
                comp_bits = comp_table.get(comp, "0000000")  # Default to NOP (invalid case)
                dest_bits = dest_table.get(dest, "000")
                jump_bits = jump_table.get(jump, "000")

                log.write(f"  Binary: comp={comp_bits}, dest={dest_bits}, jump={jump_bits}\n")

                # Construct the full machine language instruction
                MachineLanguage[3:10] = list(comp_bits)
                MachineLanguage[10:13] = list(dest_bits)
                MachineLanguage[13:16] = list(jump_bits)

            file.write("".join(MachineLanguage) + "\n")
            log.write(f"  Machine Language: {''.join(MachineLanguage)}\n\n")

            line_number += 1

    print(f"Assembly completed successfully! Output written to {output_file}")
    print(f"Conversion details written to {log_file}")

except FileNotFoundError:
    print(f"Error: Could not find file '{asmFile}'")
except IOError:
    print("Error: Could not read the file")