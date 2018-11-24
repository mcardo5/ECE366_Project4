# ECE 366 - Project 4
# Group Members: Joseph de Joya, Martin Cardoza

def hex_to_bin(hex_arr, bin_arr):
    # Start hex to bin conversion.
    for i in range(0, len(hex_arr)):
        bin_arr.append(hex_arr[i][2:len(hex_arr[i])])
        bin_arr[i] = format(int(bin_arr[i], 16), "032b")


def main():

    verbose = True

    # Prompt user for input.
    while (True):
        print("Choose Instruction Memory to be used in the simulation")
        print("e.g. i_mem_A1")
        #filename = input("Instruction Memory Filename: ")
        filename = "i_mem_A1.txt"

        # Check if the file exist
        try:
            # Attempt to open file.
            i_mem = open(filename, "r")
            print(filename + " opened successfully")
            
            # Read file.
            instr_hex = i_mem.readlines()
            
            # Remove newline character
            for i in range(0, len(instr_hex)):
                instr_hex[i] = instr_hex[i][0:len(instr_hex[i]) - 1]

            # Close instruction memory file.
            i_mem.close()
            print("")
            break
        except FileNotFoundError:
            print("Error: " + filename + " does not exist.\n")


    # Display instruction memory in Hex.
    if (verbose):
        print("Instruction Memory in Hexadecimal:")
        for i in range(0, len(instr_hex)):
            print(instr_hex[i])
        print("")

    # Convert hex to binary
    instr_bin = []
    hex_to_bin(instr_hex, instr_bin)

    if (verbose):
        print("Instruction Memory in Binary:")
        for i in range(0, len(instr_bin)):
            print(instr_bin[i])
            print(isinstance(instr_bin[i], str))
            print(format(int(instr_bin[i][16:len(instr_bin[i])], 2), "0x"))



        
    print("Complete")



if __name__ == '__main__':
    main()
