def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    if lines1 == lines2:
        print("The files are identical.")
    else:
        print("The files are different.")
        # Print the differences with line numbers
        for i, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
            if line1 != line2:
                print(f"Line {i}:")
                print(f"File 1: {line1.strip()}")
                print(f"File 2: {line2.strip()}")
                print("-" * 50)

# Example usage
path = "/Users/jacemhagui/Desktop/Academia/Coursera/NAND2TETRIS/Building-a-Computer-from-Scratch/6. Assembler/Project 6/Assembler/"
compare_files(path + "Rect.hack", path + "Rect_Correct.hack")