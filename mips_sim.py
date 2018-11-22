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
		line = format(int(line,16), "032b")
		Instructions_in_hex.append(line)
		Instructions.append(line)
			
def mips_simulation(Instructions, Instructions_in_hex):

	print("****Starting Simulation****")
	
	Registers = [0, 0, 0, 0, 0, 0, 0, 0]
	Acc_mem = [0 for i in range(mem)]		#array to hold up to limit of mem
	PC = 0
	DIC = 0
	Cycle = 1
	threecycles = 0
	fourcycles = 0
	fivecycles = 0
	
	while True:
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
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "add $" + (int(fetch[16:21],2)) + ",$" + (int(fetch[6:11],2)) + ",$" + (int(fetch[11:16],2)))
			
		elif(fetch[:6] == '000000' and fetch[26:32] == '100010'):													
			print("Sub takes 4 cycles") 
			
			PC +=1
			Cycle +=4
			fourcycles +=1
			
			Registers[int(fetch[16:21],2)] = Registers[int(fetch[6:11],2)] - Registers[int(fetch[11:16],2)] 			#general format Rd = Rs - Rt
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "sub $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
		elif(fetch[:6] == '000000' and fetch[26:32] == '101010'):													
			print("Slt Instruction takes 4 cycles")
			
			PC +=1
			Cycle +=4
			fourcycles +=1
			
			Registers[int(fetch[16:21],2)] = 1 if Registers[int(fetch[6:11],2)] < Registers[int(fetch[11:16],2)] else 0	
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "slt $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
		elif(fetch[:6] == '000000' and fetch[26:32] == '100110'):
			print("Xor takes 4 cycles")
			
			PC +=1
			Cycle +=4
			fourcycles +=1
			
			Registers[int(fetch[16:21],2)] = Registers[int(fetch[6:11],2)] ^ Registers[int(fetch[11:16],2)]			#general format Rd = Rs ^ Rt
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "xor $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
			
	#I-type instructions start here
	
		elif(fetch[:6] == '001000'):
			print("Addi takes 4 cycles")
			
			PC +=1
			Cycle +=4
			fourcycles +=1
			imm = int(fetch[16:32],2)
			
			Registers[int(fetch[11:16],2)] = Registers[int(fetch[6:11],2)] + imm
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "addi $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
		
		elif(fetch[:6] == '000100'):
			print("Beq takes 3 cycles")
			
			PC +=1
			Cycle +=3
			threecycles +=1
			imm = int(fetch[16:32],2)
			
			PC = PC + imm if (Registers[int(fetch[6:11],2)] == Registers[int(fetch[11:16],2)]) else PC
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "beq $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))

		elif(fetch[:6] == '000101'):
			print("Bne takes 3 cycles")
			
			PC +=1
			Cycle +=3
			threecycles +=1
			imm = int(fetch[16:32],2)
			
			PC = PC + imm if (Registers[int(fetch[6:11],2)] != Registers[int(fetch[11:16],2)]) else PC
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "bne $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
		elif(fetch[:6] == '100011'):
			print("lw takes 5 cyles")
			
			if(int(fetch[30:32])%4 !=0):
				print("Instruction boundary is out of bounds, program is being exit")
				print("Error caused by: ", hex(int(fetch,2)))
				break
			
			imm = int(fetch[16:32],2)
			
			PC +=1
			Cycle +=5
			fivecycles +=1
			
			Registers[int(fetch[11:16],2)] = Acc_mem[imm + Registers[int(fetch[6:11],2)] - 8192] #loads memory
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "lw $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
		elif(fetch[:6] == '101011'):
			print("sw takes 4 cycles")
			
			if(int(fetch[30:32])%4 !=0):
				print("Instruction boundary is out of bounds, program is being exit")
				print("Error caused by: ", hex(int(fetch,2)))
				break
			
			imm = int(fetch[16:32],2)
			
			PC +=1
			Cycle +=5
			fourcycles +=1
			
			Acc_mem[imm + Registers[int(fetch[6:11],2)] - 8192] = Registers[int(fetch[11:16],2)]	#stores memory
			
			print("Cycles: " + str(Cycle))
			print("PC = " + str(PC*4) + " Instruction: 0x" + Instructions_in_hex[PC] + "sw $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)))
			
			
	print("****Simulation Finished****")
	print("Total cycles: " +str(Cycle))
	print("Dynamic Instruction Count: " + str(DIC))
	print("				" + str(threecycles) + "instructions that took 3 cycles.")
	print("				" + str(fourcycles) + "instructions that took 4 cycles.")
	print("				" + str(fivecycles) + "instructions that took 5 cycles.")
	print("Registers: " + str(Registers))
			
def main():
	hex_to_binary(input_file)
	mips_simulation(Instructions, Instructions_in_hex)

if __name__ == '__main__':
	main()		
