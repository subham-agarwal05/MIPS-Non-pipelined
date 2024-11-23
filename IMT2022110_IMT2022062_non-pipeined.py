'''
the program is contsrained to a maximum of 10 inputs and outputs
'''

#machine code for factorial of 9 with output in s2
''' 
machine_code={4194304:"00100000000100010000000000001001",
4194308:"00100000000100100000000000000001",
4194312:"00100001001010010000000000000001",
4194316:"00010001001100010000000000001000",
4194320:"00100001001010010000000000000001",
4194324:"00100000000010100000000000000001",
4194328:"00000000000100100101100000100000",
4194332:"00010001001010100000000000000011",
4194336:"00000010010010111001000000100000",
4194340:"00100001010010100000000000000001",
4194344:"00001000000100000000000000000111",
4194348:"00001000000100000000000000000011",
4194352:"00000010001100011000100000100000"}
'''

#instruction memory
machine_code={4194380:"00100001110011100000000000000001",    #sorting using bubble sort algorithm
4194384:"00100000000101100000000000000000",  
4194388:"00100001001100001111111111111111",
4194392:"00000000000010101001000000100001",
4194396:"00000000000010111001100000100001",
4194400:"00000010000101100100000000101010",
4194404:"00010001000011100000000000000110",
4194408:"10001110010011000000000000000000",
4194412:"10101110011011000000000000000000",
4194416:"00100010010100100000000000000100",
4194420:"00100010011100110000000000000100",
4194424:"00100010110101100000000000000001",
4194428:"00001000000100000000000000011000",
4194432:"00100000000101101111111111111111",
4194436:"00100001001100001111111111111110",
4194440:"00000010000101100100000000101010",
4194444:"00010001000011100000000000010001",
4194448:"00100010110101100000000000000001",
4194452:"00100000000100110000000000000000",
4194456:"00000000000010111001000000100001",
4194460:"00001000000100000000000000101000",
4194464:"00000010000101101000100000100010",
4194468:"00000010001100110100000000101010",
4194472:"00010001000011101111111111110111",
4194476:"10001110010011000000000000000000",
4194480:"10001110010011010000000000000100",
4194484:"00000001101011000100000000101010",
4194488:"00010001000011100000000000000011",
4194492:"00100010010100100000000000000100",
4194496:"00100010011100110000000000000001",
4194500:"00001000000100000000000000101000",
4194504:"10101110010011010000000000000000",
4194508:"10101110010011000000000000000100",
4194512:"00001000000100000000000000101111"}

#data memory
mem={268501184:0,      #input starts here
     268501188:0,
     268501192:0,
     268501196:0,
     268501200:0,
     268501204:0,
     268501208:0,
     268501212:0,
     268501216:0,
     268501220:0,
     268501224:0,     #output starts here
     268501228:0,
     268501232:0,
     268501236:0,
     268501240:0,
     268501244:0,
     268501248:0,
     268501252:0,
     268501256:0,
     268501260:0,
     268501264:0}

def bin_to_int(bin_str):   
    '''Converts a binary string to a signed integer'''
    if bin_str[0] == '1':  # Negative number
        bin_str = ''.join('1' if b == '0' else '0' for b in bin_str)  # Flip bits
        return -1 * (int(bin_str, 2) + 1)  # Add 1 and negate
    else:  # Positive number
        return int(bin_str, 2)

#control signals
RegDst=0
Branch=0
MemRead=0
MemtoReg=0
ALUOp=00
MemWrite=0
ALUSrc=0
RegWrite=0
Jump=0

#data
reg=[0]*32
PC=4194380  #PC initialized to the starting address of the program
#PC=4194304  #for factorial code
clk_cycles=0

def control(opcode):
    '''Sets the control signals according to the opcode'''
    global RegDst,Branch,MemRead,MemtoReg,ALUOp,MemWrite,ALUSrc,RegWrite,Jump
    if(opcode=="000000"): #R-type
        RegDst=1
        Branch=0
        MemRead=0
        MemtoReg=0
        ALUOp=10
        MemWrite=0
        ALUSrc=0
        RegWrite=1
        Jump=0
    elif(opcode=="000010"): #j-type
        RegDst=0
        Branch=0
        MemRead=0
        MemtoReg=0
        ALUOp=00
        MemWrite=0
        ALUSrc=0
        RegWrite=0
        Jump=1
    elif(opcode=="001000"): #addi
        RegDst=0
        Branch=0
        MemRead=0
        MemtoReg=0
        ALUOp=00
        MemWrite=0
        ALUSrc=1
        RegWrite=1
        Jump=0
    elif(opcode=="000100"): #beq
        RegDst=0
        Branch=1
        MemRead=0
        MemtoReg=0
        ALUOp=1
        MemWrite=0
        ALUSrc=0
        RegWrite=0
        Jump=0
    elif(opcode=="100011"): #lw
        RegDst=0
        Branch=0
        MemRead=1
        MemtoReg=1
        ALUOp=00
        MemWrite=0
        ALUSrc=1
        RegWrite=1
        Jump=0
    elif(opcode=="101011"): #sw
        RegDst=0
        Branch=0
        MemRead=0
        MemtoReg=0
        ALUOp=00
        MemWrite=1
        ALUSrc=1
        RegWrite=0
        Jump=0
    
def ALUControlUnit(ALUOp,funct):
    '''Returns the ALU control signal according to the ALUOp and funct field'''
    if(ALUOp==00): #lw,sw,addi
        return "010"
    elif(ALUOp==1): #beq
        return "011"
    elif(ALUOp==10): #R-type
        if(funct=="100000"): #add
            return "010"
        elif(funct=="100010"): #sub
            return "011"
        elif(funct=="101010"): #slt
            return "100"
        elif(funct=="100001"): #addu
            return "010"

def fetch():
    '''fetches the instruction from the instruction memory and returns it'''
    global PC
    global clk_cycles
    clk_cycles+=1
    inst= machine_code[PC]
    PC=PC+4
    return inst

def decode(inst):
    '''decodes the instruction and returns the opcode,rs,rt,rd,shamt,funct,target,imm'''
    global clk_cycles
    opcode,rs,rt,rd,shamt,funct,target,imm="","","","","","","",""
    opcode=inst[0:6]
    control(opcode)
    clk_cycles+=1
    if(opcode=="000000"): #R-type
        rs=inst[6:11]
        rt=inst[11:16]
        rd=inst[16:21]
        shamt=inst[21:26]
        funct=inst[26:32]
        return opcode,rs,rt,rd,shamt,funct,target,imm
    elif(opcode=="000010"): #j-type
        target=inst[6:32]+"00"
        return opcode,rs,rt,rd,shamt,funct,target,imm
    else: #I-type
        rs=inst[6:11]
        rt=inst[11:16]
        imm=inst[16:32]
        return opcode,rs,rt,rd,shamt,funct,target,imm
    
def execute(rs,rt,imm,funct,target):
    '''executes the instruction and returns the output of the ALU'''
    global clk_cycles,PC,ALUSrc,ALUOp,Branch,Jump,RegDst,reg
    clk_cycles+=1
    ALU_out=0
    ALUcontrol=ALUControlUnit(ALUOp,funct) #control signal for ALU
    if(Jump==1): #j-type
        PC=int(target,2)
        return 0
    if(rs!=""):
        ALU_in1=reg[int(rs,2)] #first input to ALU
    if(ALUSrc==0):
        if(rt!=""):
            ALU_in2=reg[int(rt,2)]  #second input to ALU
    else:
        ALU_in2=bin_to_int(imm)
    if(ALUcontrol=="010"): #add
        ALU_out=ALU_in1+ALU_in2
    elif(ALUcontrol=="011"): #sub
        ALU_out=ALU_in1-ALU_in2
    elif(ALUcontrol=="100"): #slt
        if(ALU_in1<ALU_in2):
            ALU_out=1
        else:
            ALU_out=0
    #print("ALU_out: ",ALU_out)
    if(ALU_out==0 and Branch==1): #branch
        #print("PC branch",PC)
        PC=PC+4*bin_to_int(imm)
    return ALU_out

def memory(ALU_out,w_data):
    '''read and write from/to the data memory and returns the data for writeback'''
    global clk_cycles,MemRead,MemWrite,MemtoReg,mem
    clk_cycles+=1
    if(MemRead==1): #lw
        return mem[ALU_out]
    elif(MemWrite==1): #sw
        mem[ALU_out]=reg[int(w_data,2)]
    if(MemtoReg==0): 
        return ALU_out
    elif(MemtoReg==1):
        return mem[ALU_out]
    
    
def writeback(rt,rd,data):
    '''writes the data to the register file'''
    global clk_cycles,RegWrite,RegDst,reg
    clk_cycles+=1
    if(RegWrite==1): #write to register file
        if(RegDst==1): #R-type
            reg[int(rd,2)]=data
        else: #I-type
            reg[int(rt,2)]=data
    else:
        pass #do nothing(no writeback)

#taking input for number of integers to be sorted
n=int(input("Enter the number of inputs: "))
#initializing the registers and memory according to machine code
reg[9]=n #n is stored in $t1
reg[10]=268501184 #starting address of input
reg[11]=268501224 #starting address of output
for i in range(n): #taking integer inputs
    mem[268501184+4*i]=int(input("Enter input: "))
while(True):
    #print("PC MAchine_C: ",PC,machine_code[PC])
    inst=fetch()
    opcode,rs,rt,rd,shamt,funct,target,imm=decode(inst)
    #print("opcode: ",opcode+"rs: ",rs+"rt: ",rt+"rd: ",rd+"shamt: ",shamt+"funct: ",funct+"target: ",target+"imm: ",imm)
    ALU_out=execute(rs,rt,imm,funct,target)
    data=memory(ALU_out,rt)
    #print(mem)
    writeback(rt,rd,data)
    #print(reg)
    if(PC>4194512): #end of program
        break

print("The sorted array is: ") #printing the sorted array stored in the output address
for i in range(n):
    print(mem[268501224+4*i])
print("Number of clock cycles: ",clk_cycles) #printing the number of clock cycles


#main for factorial code
"""
while(True):
    inst=fetch()
    opcode,rs,rt,rd,shamt,funct,target,imm=decode(inst)
    ALU_out=execute(rs,rt,imm,funct,target)
    data=memory(ALU_out,rt)
    writeback(rt,rd,data)
    if(PC>4194352):
        break
print(reg[18]) #as the output is stored in $s2
"""