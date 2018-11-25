# ECE 366 - Project 4
# Group Members: Joseph de Joya, Martin Cardoza

verbose = True


def mips_add(Rs, Rt, Rd, register):
    # Function: $Rd = $Rs + $Rt
    op1 = register[Rs]
    op1.replace('0x', '')
    op2 = register[Rt]
    op2.replace('0x', '')
    val = twos_comp(int(op1, 16), 32) + twos_comp(int(op2, 16), 32)
    print(val)
    register[Rd] = dec_to_bit_hex(val) 

def mips_sub(Rs, Rt, Rd, register):
    # Function: $Rd = $Rs - $Rt
    op1 = register[Rs]
    op1.replace('0x', '')
    op2 = register[Rt]
    op2.replace('0x', '')
    val = twos_comp(int(op1, 16), 32) - twos_comp(int(op2, 16),32)
    register[Rd] = dec_to_bit_hex(val)

def mips_addi(Rs, Rt, imm, register):
    # Function: $Rt = $Rt + imm
    op1 = register[Rs]
    op1.replace('0x', '')
    val = twos_comp(int(op1, 16), 32) + imm
    register[Rt] = dec_to_bit_hex(val) 

def mips_sw(Rs, Rt, imm, d_mem, register):
    # Function: d_mem[$Rs + imm] = $Rt
    val = register[Rt]
    val.replace('0x', '')
    op1 = register[Rs]
    op1.replace('0x', '')
    mem_addr = '0x' + format(int(op1, 16) + imm, '04x')
    d_mem[mem_addr] = '0x' + format(int(val, 16), '08x')

def mips_lw(Rs, Rt, imm, d_mem, register):
    # Function: $Rt = d_mem[$Rs + imm]
    op1 = register[Rs]
    op1.replace('0x', '')
    mem_addr = '0x' + format(int(op1, 16) + imm, '04x')
    register[Rt] = d_mem[mem_addr]


def mips_beq(Rs, Rt, imm, pc, register):
    # Function: if $Rs == $Rt then PC = PC + 4 + imm
    #                         else PC = PC + 4
    # At this point PC = PC + 4, pre calculated. Thus, add imm to PC
    # if $Rs == $Rt
    if (register[Rs] == register[Rt]):
        pc.replace('0x', '')
        pc = '0x' + format(int(pc, 16) + (imm << 2), "04x")
    return pc

def mips_bne(Rs, Rt, imm, pc, register):
    # Function: if $Rs != $Rt then PC = PC + 4 + imm
    #                         else PC = PC + 4
    # At this point PC = PC + 4, pre calculated. Thus, add imm to PC
    # if $Rs == $Rt
    if (register[Rs] != register[Rt]):
        pc.replace('0x', '')
        pc = '0x' + format(int(pc, 16) + (imm << 2), "04x")
    return pc

def mips_slt(Rs, Rt, Rd, register):
    # Function: if $Rs < $Rt, then $Rd = 1
    #                         else $Rd = 0
    op1 = register[Rs]
    op1.replace('0x','')
    op2 = register[Rt]
    op2.replace('0x','')
    if (twos_comp(int(op1, 16), 32) < twos_comp(int(op2, 16), 32)):
        print('\t\t\t\t\tHere: True')
        register[Rd] = '0x00000001'
    else:
        print('\t\t\t\tHere: False')
        register[Rd] = '0x00000000'

def instr_exe(instr, register, d_mem, pc, multi_cpu, multi_instr):
    # Update pc
    pc.replace('0x', '')
    pc = '0x' + format(int(pc, 16) + 4, "04x")

    if (instr[0:6] == '000000'):
        Rs = int(instr[6:11], 2)
        Rt = int(instr[11:16], 2)
        Rd = int(instr[16:21], 2)
        if (instr[26:len(instr)] == '100000'):
            # Instruction add
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[0] = multi_instr[0] + 1
            mips_add(Rs, Rt, Rd, register)
            if (verbose):
                print('add ${}, ${}, ${}'.format(Rd, Rs, Rt))
        elif (instr[26:len(instr)] == '100010'):
            # Instruction sub
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[1] = multi_instr[1] + 1
            mips_sub(Rs, Rt, Rd, register)
            if (verbose):
                print('sub ${}, ${}, ${}'.format(Rd, Rs, Rt))
        elif (instr[26:len(instr)] == '101010'):
            # Instruction slt
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[6] = multi_instr[6] + 1
            mips_slt(Rs, Rt, Rd, register)
            if (verbose):
                print('slt ${}, ${}, ${}'.format(Rd, Rs, Rt))
        elif (instr[26:len(instr)] == '100110'):
            # Instruction xor
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[2] = multi_instr[2] + 1
            #mips_xor(Rs, Rt, Rd, register)
            if (verbose):
                print('xor ${}, ${}, ${}'.format(Rd, Rs, Rt))
    else:
        Rs = int(instr[6:11], 2)
        Rt = int(instr[11:16], 2)
        imm = twos_comp(int(instr[16:len(instr)], 2), len(instr[16:len(instr)]))
        if (instr[0:6] == '001000'):
            # Instruction addi
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[3] = multi_instr[3] + 1
            mips_addi(Rs, Rt, imm, register)
            if (verbose):
                print('addi ${}, ${}, {}'.format(Rt, Rs, imm))
        elif (instr[0:6] == '101011'):
            # Instruction sw
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[8] = multi_instr[8] + 1
            mips_sw(Rs, Rt, imm, d_mem, register)
            if (verbose):
                print('sw ${}, 0x{}(${})'.format(Rt, format(imm, '04x'), Rs))
        elif (instr[0:6] == '000100'):
            # Instruction beq
            multi_cpu[0] = multi_cpu[0] + 1
            multi_instr[4] = multi_instr[4] + 1
            pc = mips_beq(Rs, Rt, imm, pc, register)
            if (verbose):
                print('beq ${}, ${}, {}'.format(Rs, Rt, imm))
        elif (instr[0:6] == '000101'):
            # Instruction bne
            multi_cpu[0] = multi_cpu[0] + 1
            multi_instr[5] = multi_instr[5] + 1
            pc = mips_bne(Rs, Rt, imm, pc, register)
            if (verbose):
                print('bne ${}, ${}, {}'.format(Rs, Rt, imm))
        elif (instr[0:6] == '100011'):
            # Instruction lw
            multi_cpu[2] = multi_cpu[2] + 1
            multi_instr[7] = multi_instr[7] + 1
            mips_lw(Rs, Rt, imm, d_mem, register)
            if (verbose):
                print('lw ${}, 0x{}(${})'.format(Rt, format(imm, '04x'), Rs))

    return pc

def twos_comp(val, bits):
    "Compute 2's complement."
    if ((val & (1 << (bits - 1))) != 0):
        val = val - (1 << bits)
    return val

def dec_to_bit_hex(dec):
    if (dec < 0):
        dec = dec * -1
        temp_bin = format(dec, '032b')
        temp_bin = temp_bin.replace('0','*')
        temp_bin = temp_bin.replace('1','0')
        temp_bin = temp_bin.replace('*','1')
        dec = int(temp_bin, 2) + 1
    temp_bin = format(dec, '08x')
    return '0x' + temp_bin

def init_reg(register):
    # Assume there are only 7 registers.
    for i in range(0, 8):
        register.append('0x00000000')

def disp_reg(register):
    # This functions displays the contents of the register.
    print("Registers")
    print('Number\tValue')
    for i in range(0, len(register)):
        print(format(i, 'd') + '\t' + register[i])

def disp_i_mem(i_mem):
    print("Instruction Memory")
    mem_addr = "0x0000"
    print('Addr' + '\t' + 'Content')
    for i in range(0, len(i_mem)):
        print(mem_addr + '\t' + i_mem[mem_addr])
        mem_addr.replace('0x', '')
        mem_addr = '0x' + format(int(mem_addr, 16) + 4, "04x")

def disp_d_mem(d_mem):
    print("Data Memory")
    print('Addr' + '\t' + 'Content')
    key_ordered = []
    for key in d_mem:
        key_ordered.append(key)
    key_ordered.sort()
    for i in range(0, len(key_ordered)):
        print(key_ordered[i] + '\t' + d_mem[key_ordered[i]])


def hex_to_bin(hex_dict, bin_dict):
    # Initialize Memory Address
    mem_addr = '0x0000'
    # Start hex to bin conversion.
    for i in range(0, len(hex_dict)):
        temp_instr = hex_dict[mem_addr]
        bin_dict[mem_addr] = format(int(temp_instr, 16), "032b")
        mem_addr.replace('0x', '')
        mem_addr = '0x' + format(int(mem_addr, 16) + 4, "04x")

def main():

    # Prompt user for input.
    while (True):
        print("Choose Instruction Memory to be used in the simulation")
        print("e.g. i_mem_A1")
        #filename = input("Instruction Memory Filename: ")
        filename = "i_mem_A1.txt"
        #filename = "i_mem_A2.txt"

        # Check if the file exist
        try:
            # Attempt to open file.
            i_mem = open(filename, "r")
            print(filename + " opened successfully")
            
            # Read file.
            temp_instr = i_mem.readlines()
            
            # Remove newline character.
            for i in range(0, len(temp_instr)):
                temp_instr[i] = temp_instr[i][0:len(temp_instr[i]) - 1]
            # Convert to dictionary.
            mem_addr = '0x0000'
            instr_hex = {mem_addr: ''}
            for i in range(0, len(temp_instr)):
                instr_hex[mem_addr] = temp_instr[i]
                mem_addr.replace('0x', '')
                mem_addr = '0x' + format(int(mem_addr, 16) + 4, "04x")
                

            # Close instruction memory file.
            i_mem.close()
            print("")
            break
        except FileNotFoundError:
            print("Error: " + filename + " does not exist.\n")


    # Display instructions in Hex.
    if (verbose):
        disp_i_mem(instr_hex)
        #print("Instruction Memory in Hexadecimal:")
        #for i in range(0, len(instr_hex)):
        #    print('    ' + instr_hex[i])
        print("")

    # Convert hex to binary
    # Store the instructions in a dictionary with the key as the memory address
    # and the instruction the the value.
    instr_bin = {'0x0000': ''}
    hex_to_bin(instr_hex, instr_bin)

    # Display instructions in Binary.
    if (verbose):
        disp_i_mem(instr_bin)
    
    # Initialize registers.
    # All registers are initialized at zero.
    print('');
    register = [];
    init_reg(register)

    # Start Simulation
    # Test Add
    
    pc = '0x0000'
    d_mem = {'0x2000': '0x00000000', '0x2020': '0x00000000'}
    instr_count = 0
    # Statistics for MIPS multicycle implementation
    # Record breakdown of 3 / 4 / 5 cycles instruction
    # multi_cpu[0] = Number of 3 cycle instructions used
    # multi_cpu[1] = Number of 4 cycle instructions used
    # multi_cpu[2] = Number of 5 cycle instructions used
    multi_cpu = [0, 0, 0]
    # Record breakdown per instruction.
    # multi_instr[0] = number of add
    # multi_instr[1] = number of sub
    # multi_instr[2] = number of xor
    # multi_instr[3] = number of addi
    # multi_instr[4] = number of beq
    # multi_instr[5] = number of bne
    # multi_instr[6] = number of slt
    # multi_instr[7] = number of lw
    # multi_instr[8] = number of sw
    multi_instr = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    while (True):
        old_pc = pc
        pc = instr_exe(instr_bin[pc], register, d_mem, pc, multi_cpu, multi_instr)
        instr_count = instr_count + 1
        #disp_reg(register)
        #disp_d_mem(d_mem)
        if (old_pc == pc):
            break

    # Summary
    print('')
    print('-------------------------')
    print('---------Summary---------')
    print('-------------------------')
    print('PC: ' + pc)
    print('Dynamic Instruction Count: {}'.format(instr_count))
    print('')
    disp_reg(register)
    print('')
    print('Multi-cycle MIPS CPU')
    multi_total = (multi_cpu[0]*3) + (multi_cpu[1]*4) + (multi_cpu[2]*5)
    print('\ti. Total number of cycles: {}'.format(multi_total))
    print('\t\tInstruction Length\t# Cycles\t% Cycle')
    print('\t\t3 Cycles\t\t{}\t\t{:.2f}%'.format(multi_cpu[0]*3, ((multi_cpu[0]*3) / multi_total) * 100))
    print('\t\t4 Cycles\t\t{}\t\t{:.2f}%'.format(multi_cpu[1]*4, ((multi_cpu[1]*4) / multi_total) * 100))
    print('\t\t5 Cycles\t\t{}\t\t{:.2f}%'.format(multi_cpu[2]*5, ((multi_cpu[2]*5) / multi_total) * 100))
    print('\tii. Instruction Information')
    print('\t3 Cycle Instructions:')
    print('\t\tInstruction\t# Cycles\t% Cycle')
    print('\t\tbeq\t\t{}\t\t{:.2f}%'.format(multi_instr[4]*3, ((multi_instr[4]*3) / multi_total) * 100))
    print('\t\tbne\t\t{}\t\t{:.2f}%'.format(multi_instr[5]*3, ((multi_instr[5]*3) / multi_total) * 100))
    print('\t4 Cycle Instructions:')
    print('\t\tInstruction\t# Cycles\t% Cycle')
    print('\t\tadd\t\t{}\t\t{:.2f}%'.format(multi_instr[0]*4, ((multi_instr[0]*4) / multi_total) * 100))
    print('\t\tsub\t\t{}\t\t{:.2f}%'.format(multi_instr[1]*4, ((multi_instr[1]*4) / multi_total) * 100))
    print('\t\txor\t\t{}\t\t{:.2f}%'.format(multi_instr[2]*4, ((multi_instr[2]*4) / multi_total) * 100))
    print('\t\taddi\t\t{}\t\t{:.2f}%'.format(multi_instr[3]*4, ((multi_instr[3]*4) / multi_total) * 100))
    print('\t\tslt\t\t{}\t\t{:.2f}%'.format(multi_instr[6]*4, ((multi_instr[6]*4) / multi_total) * 100))
    print('\t\tsw\t\t{}\t\t{:.2f}%'.format(multi_instr[8]*4, ((multi_instr[8]*4) / multi_total) * 100))
    print('\t5 Cycle Instructions:')
    print('\t\tInstruction\t# Cycles\t% Cycle')
    print('\t\tlw\t\t{}\t\t{:.2f}%'.format(multi_instr[7]*5, ((multi_instr[7]*5) / multi_total) * 100))
    print('Pipelined MIPS CPU')
    
        
    print("Complete")



if __name__ == '__main__':
    main()
