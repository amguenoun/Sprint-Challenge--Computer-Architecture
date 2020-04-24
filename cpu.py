import sys


class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branchtable = {}
        self.branchtable[0b10000010] = self.handle_LDI
        self.branchtable[0b01000111] = self.handle_PRN
        self.branchtable[0b00000001] = self.handle_HLT

    def load(self):
        """Load a program into memory."""

        address = 0

        filename = sys.argv[1] + '.ls8'

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
