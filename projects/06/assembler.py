import re, sys

class Assembler:

    COMP = {
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        'M': '1110000',
        '!M': '1110001',
        '-M': '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101'
    }

    DEST = {
        'null': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'
    }

    JUMP = {
        'null': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }

    def __init__(self) -> None:
        self.symbol_table = {
            'SCREEN': 16384,
            'KBD': 24576,
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4
        }
        for i in range(16):
            self.symbol_table['R' + str(i)] = i
        self.code = None
        self.hack_lines = None
        self.file_path = sys.argv[1]
        self.binary_code = None


    def parse_file(self):
        code = []
        with open(self.file_path, 'r') as file:
            lines_code = file.readlines()
        for line in lines_code:
            print(line)
            line = re.sub('//.*', '', line)
            line = line.strip()
            if line:
                code.append(line)
            self.code = code

    
    def first_pass(self):
        rom_address = 0
        for line in self.code:
            if line.startswith('(') and line.endswith(')'):
                symbol = line[1:-1]
                self.symbol_table[symbol] = rom_address
            else:
                rom_address += 1

    
    def second_pass(self):
        ram_address_var = 16
        for line in self.code:
            if line.startswith('@'):
                symbol = line[1:]
                if not symbol.isdigit() and symbol not in self.symbol_table:
                    self.symbol_table[symbol] = ram_address_var
                    ram_address_var += 1
    

    def third_pass(self):
        binary_code = []
        for line in self.code:
            if line.startswith('@'):
                symbol = line[1:]
                binary_code.append(self.handle_a_instruction(symbol)) # Complet
            elif not (line.startswith('(') and line.endswith(')')):
                binary_code.append(self.handle_c_instruction(line)) # Complete
        self.binary_code = binary_code
    

    def handle_c_instruction(self, line):
        dest = comp = jump = 'null'
        if '=' in line:
            dest, line = line.split('=')
        if ';' in line:
            comp, jump = line.split(';')
        else:
            comp = line
        return '111' + self.COMP[comp] + self.DEST[dest] + self.JUMP[jump]
    
    
    def handle_a_instruction(self, symbol):
        if symbol.isdigit():
            return format(int(symbol), '016b')
        else:
            return format(self.symbol_table[symbol], '016b')
    
    
    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            for line in self.binary_code:
                f.write(line + '\n')


if __name__ == '__main__':
    assembler = Assembler()
    input_file = sys.argv[1]
    output_file = input_file.split('.')[0] + '.hack'
    
    print(f"Reading file: {input_file}")
    assembler.parse_file()
    
    print("Performing first pass...")
    assembler.first_pass()
    
    print("Performing second pass...")
    assembler.second_pass()
    
    print("Performing third pass...")
    assembler.third_pass()
    
    print(f"Writing to file: {output_file}")
    assembler.write_to_file(output_file)
    
    print("Program completed successfully")


