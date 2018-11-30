# ECE 366 - Project 4
# Group Members: Joseph de Joya, Martin Cardona

verbose = True


def mips_add(Rs, Rt, Rd, register):
    # Function: $Rd = $Rs + $Rt
    op1 = register[Rs]
    op2 = register[Rt]
    val = twos_comp(int(op1, 16), 32) + twos_comp(int(op2, 16), 32)
    register[Rd] = dec_to_bit_hex(val) 

def mips_sub(Rs, Rt, Rd, register):
    # Function: $Rd = $Rs - $Rt
    op1 = register[Rs]
    op2 = register[Rt]
    val = twos_comp(int(op1, 16), 32) - twos_comp(int(op2, 16),32)
    register[Rd] = dec_to_bit_hex(val)

def mips_addi(Rs, Rt, imm, register):
    # Function: $Rt = $Rt + imm
    op1 = register[Rs]
    val = twos_comp(int(op1, 16), 32) + imm
    register[Rt] = dec_to_bit_hex(val) 

def mips_sw(Rs, Rt, imm, d_mem, register):
    # Function: d_mem[$Rs + imm] = $Rt
    val = register[Rt]
    op1 = register[Rs]
    mem_addr = '0x' + format(int(op1, 16) + imm, '04x')
    d_mem[mem_addr] = '0x' + format(int(val, 16), '08x')

def mips_lw(Rs, Rt, imm, d_mem, register, cache):
    # Function: $Rt = d_mem[$Rs + imm]
    op1 = register[Rs]
    mem_addr = '0x' + format(int(op1, 16) + imm, '04x')
    # Cache Statistics
    mem_addr_bin  = format(int(op1, 16) + imm, '016b')
    access = cache[len(cache) - 1]
    miss = cache[len(cache) - 2]
    hit = cache[len(cache) - 3]
    dmS4B2 = cache[0]
    dmS2B4 = cache[1]
    faS2B4 = cache[2]
    saS2B8 = cache[3]
    # a. Direct Mapped, blk sz 4, # blk 2
    try:
        register[Rt] = d_mem[mem_addr]
        valid = '1'
    except KeyError:
        d_mem[mem_addr] = '0x00000000'
        register[Rt] = d_mem[mem_addr]
        valid = '0'
    tag = mem_addr_bin[0:11]
    tagfa = mem_addr_bin[0:13]
    blk1 = mem_addr_bin[11]
    offset1 = mem_addr_bin[12:len(mem_addr_bin) - 2]
    blk2 = mem_addr_bin[11:13]
    offset2 = mem_addr_bin[13]
    set_idx = mem_addr_bin[11:13]
    if (access == 0):
        miss[0] = miss[0] + 1
        miss[1] = miss[1] + 1
        miss[2] = miss[2] + 1
        miss[3] = miss[3] + 1
        saCache_new = {'': ''}
        for i in range(0,4):
            saCache_new[format(i, '02b')] = ['Empty', 'Empty']
        saCache_new[set_idx][0] = tag
        del saCache_new['']
        faCache_new = [tagfa, 'Empty', 'Empty', 'Empty']
    else:
        # For DM1 Cache Setting
        if ((dmS4B2[access-1][3] == blk1) and (valid == '1') and (dmS4B2[access-1][2] == tag)):
            hit[0] = hit[0] + 1
        else:
            miss[0] = miss[0] + 1
        
        # For DM2 Cache Setting
        if ((dmS2B4[access-1][3] == blk2) and (dmS2B4[access-1][1] == valid) and (dmS2B4[access-1][2] == tag)):
            hit[1] = hit[1] + 1
        else:
            miss[1] = miss[1] + 1

        # For SA Cache Setting
        saCache = saS2B8[access-1][3]
        saCache_new = {'': ''}
        for i in range(0,4):
            saCache_new[format(i, '02b')] = [saCache[format(i, '02b')][0], saCache[format(i, '02b')][1]]
        del saCache_new['']
        if ((valid == '1') and ((saCache[set_idx][0] == tag) or (saCache[set_idx][1] == tag))):
            hit[3] = hit[3] + 1
        else:
            # Update Cache
            if (saCache[set_idx][0] == 'Empty'):
                saCache_new[set_idx][0] = tag
            elif (saCache[set_idx][1] == 'Empty'):
                saCache_new[set_idx][1] = tag
            else:
                saCache_new[set_idx][0] = tag
            miss[3] = miss[3] + 1

        # For FA Cache Setting
        faCache = faS2B4[access-1][2]
        faCache_new = [faCache[0], faCache[1], faCache[2], faCache[3]]
        if ((valid == '1') and ((faCache[0] == tagfa) or (faCache[1] == tagfa) or (faCache[2] == tagfa) or (faCache[3] == tagfa))):
            hit[2] = hit[2] + 1
        else:
            # Update Cache
            if (faCache[1] == 'Empty'):
                faCache_new[1] = tagfa
            elif (faCache[2] == 'Empty'):
                faCache_new[2] = tagfa
            elif (faCache[3] == 'Empty'):
                faCache_new[3] = tagfa
            else:
                faCache_new[0] = tagfa
            miss[2] = miss[2] + 1
        
    dmS4B2.append([mem_addr, valid, tag, blk1, offset1])
    dmS2B4.append([mem_addr, valid, tag, blk2, offset2])
    saS2B8.append([mem_addr, valid, set_idx, saCache_new, offset2])
    faS2B4.append([mem_addr, valid, faCache_new, offset2])

    access = access + 1
    # Update record
    cache[len(cache) - 1] = access
    cache[len(cache) - 2] = miss
    cache[len(cache) - 3] = hit
    cache[0] = dmS4B2
    cache[1] = dmS2B4
    cache[2] = faS2B4
    cache[3] = saS2B8

def mips_beq(Rs, Rt, imm, pc, register):
    # Function: if $Rs == $Rt then PC = PC + 4 + imm
    #                         else PC = PC + 4
    # At this point PC = PC + 4, pre calculated. Thus, add imm to PC
    # if $Rs == $Rt
    if (register[Rs] == register[Rt]):
        pc = '0x' + format(int(pc, 16) + (imm << 2), "04x")
        
    return pc

def mips_bne(Rs, Rt, imm, pc, register):
    # Function: if $Rs != $Rt then PC = PC + 4 + imm
    #                         else PC = PC + 4
    # At this point PC = PC + 4, pre calculated. Thus, add imm to PC
    # if $Rs == $Rt
    if (register[Rs] != register[Rt]):
        pc = '0x' + format(int(pc, 16) + (imm << 2), "04x")
    return pc

def mips_slt(Rs, Rt, Rd, register):
    # Function: if $Rs < $Rt, then $Rd = 1
    #                         else $Rd = 0
    op1 = register[Rs]
    op2 = register[Rt]
    if (twos_comp(int(op1, 16), 32) < twos_comp(int(op2, 16), 32)):
        register[Rd] = '0x00000001'
    else:
        register[Rd] = '0x00000000'

def mips_xor(Rs, Rt, Rd, register):
    # Function: $Rd = $Rs xor $Rt
    op1 = format(int(register[Rs], 16), '032b')
    op2 = format(int(register[Rt], 16), '032b')
    result = []
    for i in range(0,len(op1)):
        if (op1[i] == op2[i]):
            result.append('0')
        else:
            result.append('1')

    register[Rd] = '0x' + format(int(''.join(result), 2), '08x')

def instr_exe(instr, register, d_mem, pc, multi, cache):
    # Update pc
    pc = '0x' + format(int(pc, 16) + 4, "04x")
    multi_cpu = multi[0]
    multi_instr = multi[1]
    #total_pipeline = pipe[0]		#keeps track of pipeline cycles
    #total_hazard = hazard[[0],[1]]	#hazard 0 is for a register and 1 is for the dynamic instruction count(DIC)
    

    if (instr[0:6] == '000000'):
        Rs = int(instr[6:11], 2)
        Rt = int(instr[11:16], 2)
        Rd = int(instr[16:21], 2)
        if (instr[26:len(instr)] == '100000'):
            # Instruction add
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[0] = multi_instr[0] + 1
            #pipe[0] +=1
            #hazard[0] = Rd
            #hazard[1] = instr_count
            mips_add(Rs, Rt, Rd, register)
            if (verbose):
                print('add ${}, ${}, ${}'.format(Rd, Rs, Rt))
        elif (instr[26:len(instr)] == '100010'):
            # Instruction sub
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[1] = multi_instr[1] + 1
            #pipe[0] +=1
            #hazard[0] = Rd
            #hazard[1] = instr_count 
            mips_sub(Rs, Rt, Rd, register)
            if (verbose):
                print('sub ${}, ${}, ${}'.format(Rd, Rs, Rt))
        elif (instr[26:len(instr)] == '101010'):
            # Instruction slt
            #pipe[0] +=1
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[6] = multi_instr[6] + 1
            mips_slt(Rs, Rt, Rd, register)
            if (verbose):
                print('slt ${}, ${}, ${}'.format(Rd, Rs, Rt))
        elif (instr[26:len(instr)] == '100110'):
            # Instruction xor
            multi_cpu[1] = multi_cpu[1] + 1
            multi_instr[2] = multi_instr[2] + 1
            #pipe[0] +=1
            #hazard[0] = Rd
            #hazard[1] = instr_count
            mips_xor(Rs, Rt, Rd, register)
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
            #pipe[0] +=1
            #hazard[0] = Rt
            #hazard[1] = instr_count
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
            mips_lw(Rs, Rt, imm, d_mem, register, cache)
            if (verbose):
                print('lw ${}, 0x{}(${})'.format(Rt, format(imm, '04x'), Rs))

    # Update statistics
    multi[0] = multi_cpu
    multi[1] = multi_instr
    #total_pipeline = pipe[0]
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
        mem_addr = '0x' + format(int(mem_addr, 16) + 4, "04x")

def disp_d_mem(d_mem):
    print("Data Memory")
    print('Addr' + '\t' + 'Content')
    try:
        del d_mem['']
    except KeyError:
        d_mem = d_mem
    
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
        mem_addr = '0x' + format(int(mem_addr, 16) + 4, "04x")

def main():

    # Prompt user for input.
    while (True):
        print("Choose Instruction Memory to be used in the simulation")
        print("e.g. i_mem_A1")
        filename = input("Instruction Memory Filename: ")
        # For testing purposes
        #filename = "i_mem_A1.txt"
        #filename = "i_mem_A2.txt"
        filename = "i_mem_B1.txt"
        #filename = "i_mem_B2.txt"

        # Check if the file exist
        try:
            # Attempt to open file.
            i_mem = open(filename, "r")
					
            print(filename + " opened successfully")
            
            # Read file.
            temp_instr = i_mem.readlines()
            
            # Remove newline character.
            for i in range(0, len(temp_instr)):
                temp_instr[i] = temp_instr[i].replace('\n', '')
            # Convert to dictionary.
            mem_addr = '0x0000'
            instr_hex = {mem_addr: ''}
            for i in range(0, len(temp_instr)):
                instr_hex[mem_addr] = temp_instr[i]
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
    d_mem = {'': ''}
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
    multi = [multi_cpu, multi_instr]
    # Record Cache Behavior
    hit = [0, 0, 0, 0]
    miss = [0, 0, 0, 0]
    access = 0
    # For direct mapped, block size: 4 words, number of blocks: 2
    dmS4B2 = []
    dmS2B4 = []
    faS2B4 = []
    saS2B8 = []
    cache = [dmS4B2, dmS2B4, faS2B4, saS2B8, hit, miss, access]
    while (True):
        old_pc = pc
        #total_pipeline = pipe[0]
        pc = instr_exe(instr_bin[pc], register, d_mem, pc, multi, cache)
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
   # print('Total Pipelined Cycles: ' + total_pipeline)
    #print('Hazards Detected: ' + hazard[0] + hazard[1])
    print('Cache Access Behavior')
    hit = cache[len(cache) - 3]
    miss = cache[len(cache) - 2]
    print('\ta. Direct Mapped Cache, block size: 4 words, number of blocks: 2')
    print('\tCache log')
    for i in range(0, len(cache[0])):
        print('\t\tlw access: {}'.format(i+1))
        print('\t\t\tMem Addr: ' + cache[0][i][0])
        print('\t\t\tValid bit: ' + cache[0][i][1])
        print('\t\t\tTag: ' + cache[0][i][2])
        print('\t\t\tBlk Index: {}'.format(int(cache[0][i][3], 2)))
        print('\t\t\tOffset: {:.0f}'.format(int(cache[0][i][4], 2)))
    print('\t\tNumber of Hits: {}'.format(hit[0]))
    print('\t\tNumber of Misses: {}'.format(miss[0]))
    print('\t\tHit Rate: {:.2f}%'.format((hit[0] / (hit[0] + miss[0]) * 100)))
    print('\tb. Direct Mapped Cache, block size: 2 words, number of blocks: 4')
    print('\tCache log')
    for i in range(0, len(cache[1])):
        print('\t\tlw access: {}'.format(i+1))
        print('\t\t\tMem Addr: ' + cache[1][i][0])
        print('\t\t\tValid bit: ' + cache[1][i][1])
        print('\t\t\tTag: ' + cache[1][i][2])
        print('\t\t\tBlk Index: {}'.format(int(cache[1][i][3], 2)))
        print('\t\t\tOffset: {:.0f}'.format(int(cache[1][i][4], 2)))
    print('\t\tNumber of Hits: {}'.format(hit[1]))
    print('\t\tNumber of Misses: {}'.format(miss[1]))
    print('\t\tHit Rate: {:.2f}%'.format((hit[1] / (hit[1] + miss[1]) * 100)))
    print('\tc. Fully-Associated Cache, block size: 2 words, number of blocks: 4')
    for i in range(0, len(cache[2])):
        print('\t\tlw access: {}'.format(i+1))
        print('\t\t\tMem Addr: ' + cache[2][i][0])
        print('\t\t\tValid bit: ' + cache[2][i][1])
        print('\t\t\tWay/Block 1 Tag: ' + cache[2][i][2][0])
        print('\t\t\tWay/Block 2 Tag: ' + cache[2][i][2][1])
        print('\t\t\tWay/Block 3 Tag: ' + cache[2][i][2][2])
        print('\t\t\tWay/Block 4 Tag: ' + cache[2][i][2][3])
        print('\t\t\tOffset: {:.0f}'.format(int(cache[2][i][3], 2)))
    print('\t\tNumber of Hits: {}'.format(hit[2]))
    print('\t\tNumber of Misses: {}'.format(miss[2]))
    print('\t\tHit Rate: {:.2f}%'.format((hit[2] / (hit[2] + miss[2]) * 100)))
    print('\td. 2-Way Set-Associative Cache, block size: 2 words, number of blocks: 8, number of sets: 4')
    for i in range(0, len(cache[3])):
        print('\t\tlw access: {}'.format(i+1))
        print('\t\t\tMem Addr: ' + cache[3][i][0])
        print('\t\t\tValid bit: ' + cache[3][i][1])
        set_idx = cache[3][i][2]
        print('\t\t\tSet Index: {}'.format(int(set_idx, 2)))
        print('\t\t\tWay A Tag: ' + cache[3][i][3][set_idx][0])
        print('\t\t\tWay B Tag: ' + cache[3][i][3][set_idx][1])
        print('\t\t\tOffset: {:.0f}'.format(int(cache[3][i][4], 2)))
    print('\t\tNumber of Hits: {}'.format(hit[3]))
    print('\t\tNumber of Misses: {}'.format(miss[3]))
    print('\t\tHit Rate: {:.2f}%'.format((hit[3] / (hit[3] + miss[3]) * 100)))
        

    print("Complete")
    
    


if __name__ == '__main__':
    main()
    
