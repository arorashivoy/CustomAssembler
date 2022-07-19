#
# assembler.py
# By - Shivoy Arora
#      Suhani Mathur
#      Shobhit Pandey
# Date - 30/06/2022
#

# TODO ask if we have to clear FLAGS before execution an instruction

import sys

MAX_REG = 65535


class registers:
    """ Call registers to handle the value of registers and printing them """

    def __init__(self):
        self.regs = {"000": 0, "001": 0, "010": 0, "011": 0,
                     "100": 0, "101": 0, "110": 0, "111": "0"*16, "PC": 0}

    def clearFlag(self):
        """ Clear FLAGS """
        self.regs["111"] = "0"*16

    def setOverflow(self):
        """ Set Overflow in FLAGS """
        self.regs["111"] = "0"*12 + "1" + "000"

    def setLess(self):
        """ Set less than in FLAGS """
        self.regs["111"] = "0"*13 + "1" + "00"

    def setGreater(self):
        """ Set greater than in FLAGS """
        self.regs["111"] = "0"*14 + "1" + "0"

    def setEqual(self):
        """ Set equal to in FLAGS """
        self.regs["111"] = "0"*15 + "1"

    def convBin8(self, num):
        """ Convert the num to 8 bit binary  number

            Args:
                int num: number to be converted

            Returns: 8 bit binary representation of num
        """
        binNum = bin(num)[2:]
        return "0"*(8-len(binNum)) + binNum

    def convBin16(self, num):
        """ Convert the num to 16 bit binary  number

            Args:
                int num: number to be converted

            Returns: 16 bit binary representation of num
        """
        binNum = bin(num)[2:]
        return "0"*(16-len(binNum)) + binNum

    def __repr__(self) -> str:
        return "{} {} {} {} {} {} {} {} {}".format(self.convBin8(self.regs["PC"]), self.convBin16(self.regs["000"]), self.convBin16(self.regs["001"]), self.convBin16(self.regs["010"]),
                                                   self.convBin16(self.regs["011"]), self.convBin16(self.regs["100"]), self.convBin16(self.regs["101"]), self.convBin16(self.regs["110"]), self.regs["111"])


class operation:
    """ Class operation to handle the operations to be done """

    def __init__(self, regs: registers) -> None:
        # operation of each opcode
        self.opcodes = {"10000": self.add, "10001": self.sub,  "10010": self.mov1,  "10011": self.mov2,  "10100": self.ld,  "10101": self.st,  "10110": self.mul,  "10111": self.div,  "11000": self.rs,  "11001": self.ls,
                        "11010": self.xor,  "11011": self.orOps,  "11100": self.andOps,  "11101": self.notOps,  "11110": self.cmp,  "11111": self.jmp,  "01100": self.jlt,  "01101": self.jgt,  "01111": self.je,  "01010": self.hlt}

        self.regsObj = regs
        self.regs = regs.regs

    ##### Functions of the operations that has to be done #####
    def add(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] + \
            self.regs[command[3:6]]

        # checking for overflow
        if self.regs[reg3] > MAX_REG:
            self.regsObj.setOverflow()

            self.regs[reg3] %= (MAX_REG+1)

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def sub(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] - \
            self.regs[command[3:6]]

        # checking for overflow
        if self.regs[reg3] < 0:
            self.regs[reg3] = 0
            self.regsObj.setOverflow()

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def mov1(self, command):
        # Clearing the flag
        self.regsObj.clearFlag()

        self.regs[command[:3]] = int(command[3:], 2)

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def mov2(self, command):
        # removing filler bits
        command = command[5:]

        # Clearing the flag
        self.regsObj.clearFlag()

        self.regs[command[3:]] = self.regs[command[:3]]

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def ld(self, command):
        pass

    def st(self, command):
        pass

    def mul(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] * \
            self.regs[command[3:6]]

        # checking for overflow
        if self.regs[reg3] > MAX_REG:
            self.regsObj.setOverflow()

            self.regs[reg3] %= (MAX_REG+1)

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def div(self, command):
        # removing filler bits
        command = command[5:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # quotient
        self.regs["000"] = command[:3] // command[3:]
        # remainder
        self.regs["001"] = command[:3] % command[3:]

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def rs(self, command):
        # Clearing the flag
        self.regsObj.clearFlag()

        self.regs[command[:3]] = self.regs[command[:3]] >> int(command[3:], 2)

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def ls(self, command):
        # Clearing the flag
        self.regsObj.clearFlag()

        self.regs[command[:3]] = self.regs[command[:3]] << int(command[3:], 2)

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def xor(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] ^ \
            self.regs[command[3:6]]

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def orOps(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] | \
            self.regs[command[3:6]]

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def andOps(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] & \
            self.regs[command[3:6]]

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def notOps(self, command):
        # removing filler bits
        command = command[5:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        num = bin(self.regs[command[:3]])[2:]

        invert = ["1" if i == "0" else "0" for i in num]
        self.regs[command[3:]] = int("".join(invert), 2)

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def cmp(self, command):
        # removing filler bits
        command = command[5:]

        # Setting FLAGS
        if command[:3] == command[3:]:
            self.regsObj.setEqual()
        elif command[:3] > command[3:]:
            self.regsObj.setGreater()
        elif command[:3] < command[3:]:
            self.regsObj.setLess()

        # Setting the program counter
        self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def jmp(self, command):
        # removing filler bits
        command = command[3:]

        # Setting the program counter
        self.regs["PC"] = int(command, 2)

        # printing the object
        print(self.regsObj)

    def jlt(self, command):
        # removing filler bits
        command = command[3:]

        # Checking flag
        # Setting the program counter
        if self.regs["111"][-3] == "1":
            self.regs["PC"] = int(command, 2)
        else:
            self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def jgt(self, command):
        # removing filler bits
        command = command[3:]

        # Checking flag
        # Setting the program counter
        if self.regs["111"][-2] == "1":
            self.regs["PC"] = int(command, 2)
        else:
            self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def je(self, command):
        # removing filler bits
        command = command[3:]

        # Checking flag
        # Setting the program counter
        if self.regs["111"][-1] == "1":
            self.regs["PC"] = int(command, 2)
        else:
            self.regs["PC"] += 1

        # printing the object
        print(self.regsObj)

    def hlt(self, command):
        print("hlt:", self.regs)
        exit(0)


############# Main Function #############
if __name__ == "__main__":
    ######## getting input ########
    lines = [i.strip() for i in sys.stdin.readlines()]

    ######## Creating Objects ########
    # registers
    regs = registers()

    # operations
    ops = operation(regs)

    while True:
        ops.opcodes[lines[regs.regs["PC"]][:5]](lines[regs.regs["PC"]][5:])
