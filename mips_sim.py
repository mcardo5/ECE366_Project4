#Authors: Joseph De Joya, Martin Cardona
#Instructions in mips_simulation are in order based on whether R or I type
#First 4 are R-type: add, sub, slt, xor
#Other 5 are I-type: addi, beq, bne, lw, sw

def hex_to_binary(input_file):
	
	input_file = open("i_mem.txt", "r")	
	Instructions = []			#an array which holds the instructions
	Instuctions_in_hex = []		#holds the hex value instructions
	
	for line in input_file:
		line = line.replace('\n', '')
		line = line.replace('0x', '')
		Instructions_in_hex.append(line)
		line = format(int(line,16), "032b")
		Instructions.append(line)
			

def mips_simulation(Instructions, Instructions_in_hex):

	print("****Starting Simulation****")
	
	Registers = [0, 0, 0, 0, 0, 0, 0, 0]
	PC = 0
	DIC = 0
	Cycle = 1
	threecycles = 0
	fourcycles = 0
	fivecycles = 0
	
	while(not(0)):
		DIC += 1
		fetch = Instructions[PC]
		
		#termination of program
		if(fetch[:32] == '00010000000000001111111111111111'):
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + " :Deadloop. Program has ended")
			break
			
		elif(fetch[:6] == '000000' and fetch[26:32] == '100000'):													
			print("Add takes 4 cycles")
			
			PC += 1 
			Cycle +=4
			fourcycles +=1
			Registers[int(fetch[16:21],2)] = Registers[int(fetch[6:11],2)] + Registers[int(fetch[11:16],2)]			#general fromat Rd = Rs + Rt
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "add $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
		elif(fetch[:6] == '000000' and fetch[26:32] == '100010'):													
			print("Sub takes 4 cycles") 
			
			PC +=1
			Cycle +=4
			fourcycles +=1
			Registers[int(fetch[16:21],2)] = Registers[int(fetch[6:11],2) + Registers[int(fetch[11:16],2)] 			#general format Rd = Rs - Rt
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "sub $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
		elif(fetch[:6] == '000000' and fetch[26:32] == '101010'):													
			print("Slt Instruction takes 4 cycles")
			
			PC +=1
			Cycle +=4
			fourcycles +=1
			Registers[int(fetch[16:21],2)] = 1 if Registers[int(fetch[6:11],2) < Registers[int(fetch[11:16],2)]		#general format Rd = 1 if Rs < Rt
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "slt $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
		elif(fetch[:6] == '000000' and fetch[26:32] == '100110'):
			print("Xor takes 4 cycles")
			
			PC +=1
			Cycle +=4
			fourcycles +=1
			Registers[int(fetch[16:21],2) = Registers[int(fetch[6:11],2) ^ Registers[int(fetch[11:16],2)]			#general format Rd = Rs ^ Rt
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "add $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
			
	#I-type instructions start here
	
		elif(fetch[:6] == '001000'):
			print("Addi takes 4 cycles")
			
			PC +=1
			Cycle +=4
			fourcycles +=1
			imm = [int(fetch[16:32],2)]
		
		
			
			 
	
	
