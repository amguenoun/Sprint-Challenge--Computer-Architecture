import sys


class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.FL = 0b00000000
        self.branchtable = {}
        self.branchtable[0b10000010] = self.handle_LDI
        self.branchtable[0b01000111] = self.handle_PRN
        self.branchtable[0b00000001] = self.handle_HLT
        self.branchtable[0b10100111] = self.handle_CMP
        self.branchtable[0b01010100] = self.handle_JMP
        self.branchtable[0b01010101] = self.handle_JEQ
        self.branchtable[0b01010110] = self.handle_JNE

        self.branchtable[0b10101000] = self.handle_AND
        self.branchtable[0b10101010] = self.handle_OR
        self.branchtable[0b10101011] = self.handle_XOR
        self.branchtable[0b01101001] = self.handle_NOT
        self.branchtable[0b10101100] = self.handle_SHL
        self.branchtable[0b10101101] = self.handle_SHR
        self.branchtable[0b10100100] = self.handle_MOD

    def load(self):
        """Load a program into memory."""

        address = 0

        filename = 'sctest.ls8'

        file = open(filename, 'r')
        program = []

        for line in file:
            if not line[0] == '#' and not len(line.strip()) == 0:
                program.append(int(line.strip()[:8], 2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == 'CMP':
            a = self.reg[reg_a]
            b = self.reg[reg_b]
            if a == b:
                self.FL = 0b00000001
            elif a > b:
                self.FL = 0b00000010
            elif a < b:
                self.FL = 0b00000100
        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == 'SHL':
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] >>= self.reg[reg_b]
        elif op == 'MOD':
            self.reg[reg_a] %= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def handle_HLT(self):
        sys.exit()

    def handle_LDI(self):
        reg_address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[reg_address] = value

    def handle_PRN(self):
        reg_address = self.ram[self.pc + 1]
        print(self.reg[reg_address])

    def handle_CMP(self):
        reg_address_a = self.ram[self.pc + 1]
        reg_address_b = self.ram[self.pc + 2]
        self.alu('CMP', reg_address_a, reg_address_b)

    def handle_JMP(self):
        reg_address = self.ram[self.pc + 1]
        self.pc = self.reg[reg_address]

    def handle_JEQ(self):
        eq = self.FL & 0b00000001
        if eq == 1:
            self.handle_JMP()
        else:
            self.pc += 2

    def handle_JNE(self):
        eq = self.FL & 0b00000001
        if not eq:
            self.handle_JMP()
        else:
            self.pc += 2

    def handle_AND(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('AND', reg_a, reg_b)

    def handle_OR(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('OR', reg_a, reg_b)

    def handle_XOR(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('XOR', reg_a, reg_b)

    def handle_NOT(self):
        reg_a = self.ram[self.pc + 1]
        self.alu('AND', reg_a)

    def handle_SHL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('SHL', reg_a, reg_b)

    def handle_SHR(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('SHR', reg_a, reg_b)

    def handle_SHR(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('MOD', reg_a, reg_b)

    def run(self):
        """Run the CPU."""
        self.reg[7] = 0xF4

        while True:
            # grab from memory - an instruction register
            mem = self.ram[self.pc]
            increment = ((mem & 0b11000000) >> 6) + 1
            jumping = ((mem & 0b00010000) >> 4)

            if mem in self.branchtable:
                self.branchtable[mem]()
            else:
                print(f'Intruction {mem} unknown')
                break

            if not jumping:
                self.pc += increment
