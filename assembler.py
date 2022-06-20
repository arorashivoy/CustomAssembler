#
# assembler.py
# By - Shivoy Arora
# Date - 20/06/2022
#


# opcode of each command
opcodes = {"add": "10000", "sub": "10001", "mov1": "10010", "mov2": "10011", "ld": "10100", "st": "10101", "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001",
           "xor": "11010", "or": "11011", "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111", "hlt": "01010"}

# registers binary representation
regsRepr = {"R0": "000", "R1": "001", "R2": "010", "R3": "011",
        "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

# statement types
stmtTypes = {"add": "A", "sub": "A", "mov1": "B", "mov2": "C", "ld": "D", "st": "D", "mul": "A", "div": "C", "rs": "B",
             "ls": "B", "xor": "A", "or": "A", "and": "A", "not": "C", "cmp": "C", "jmp": "E", "jlt": "E", "jgt": "E", "je": "E", "hlt": "F"}

# unused space in regard to ops type
unusedSpace = {"A": "00", "B": "", "C": "00000", "D": "", "E": "000", "F": "00000000000"}




# reading the file
with open("stdin.txt", "r") as f:
    lines = [[j.strip() for j in i.strip().split()] for i in f.readlines()]


# creating machine code lst
machineCode = []

#TODO check for variable declaration

# traversing each line
for line in range(lines):
    binLine = ""

    ops = lines[line][0]

    # converting ops to incorporate two types of mov command
    if ops == "mov":
        if lines[line][2][0] == "$":
            ops = "mov1"
        else:
            ops = "mov2"

    # adding opcode to binLine
    binLine = opcodes[ops]

    # adding unused space
    stmtType = stmtTypes[ops]
    binLine += unusedSpace[stmtType]

    # For statements with only registers and immediate values
    if stmtType == "A" and stmtType == "B" and stmtType == "C":
        for i in lines[line][1:]:

            # if registers are present
            if i[0] != "$":
                binLine += regsRepr[i]
            
            # immediate value is present
            else:
                binRepr = bin(int(i[1:]))[2:]
                binLine += "0" * (8 - len(binRepr)) + binRepr

    # For ld and st statements
    elif stmtType == "D":
        pass
