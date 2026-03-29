import sys

class Parser:
    def __init__(self, line, symbol_table):
        self.line = line.split('//')[0].strip()
        self.type = self.type_check()
        self.d = ''
        self.c = ''
        self.j = ''
        self.symbol_table = symbol_table

    def type_check(self):
        if '@' in self.line:
            return 'A'
        elif '=' in self.line or ';' in self.line:
            return 'C'
        else:
            return ''

    def parse(self):
        # handle //
        if self.type == 'A': # A-instruction
            number = self.line[1:] # remove "@"
            if number in self.symbol_table:
                number =  self.symbol_table[number]
            address = format(int(number), '016b')[1:]
            return "0" + address
        elif self.type == 'C': # C-instruction
            dest, comp, jump = '', '', ''
            if '=' in self.line:
                dest, comp = self.line.split('=')
            if ';' in self.line:
                comp, jump = self.line.split(';')
            self.d = dest
            self.c = comp
            self.j = jump
            return
        else:
            # Should be discard
            return
    
    def comp(self):
        return self.c

    def dest(self):
        return self.d

    def jump(self):
        return self.j


class Code:
    def __init__(self):
        pass

    def comp(self, c):
        comp_table = {
            # a = 0
            '0':   '0' + '101010',
            '1':   '0' + '111111',
            '-1':  '0' + '111010',
            'D':   '0' + '001100',
            'A':   '0' + '110000',
            '!D':  '0' + '001101',
            '!A':  '0' + '110001',
            '-D':  '0' + '001111',
            '-A':  '0' + '110011',
            'D+1': '0' + '011111',
            'A+1': '0' + '110111',
            'D-1': '0' + '001110',
            'A-1': '0' + '110010',
            'D+A': '0' + '000010',
            'D-A': '0' + '010011',
            'A-D': '0' + '000111',
            'D&A': '0' + '000000',
            'D|A': '0' + '010101',

            # a = 1
            'M':   '1' + '110000',
            '!M':  '1' + '110001',
            '-M':  '1' + '110011',
            'M+1': '1' + '110111',
            'M-1': '1' + '110010',
            'D+M': '1' + '000010',
            'D-M': '1' + '010011',
            'M-D': '1' + '000111',
            'D&M': '1' + '000000',
            'D|M': '1' + '010101',
        }
        return comp_table[c]
    
    def dest(self, d):
        dest_table = {
            'M': '001',
            'D': '010',
            'MD': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111',
        }
        if d in dest_table:
            return dest_table[d]
        return '000'
    
    def jump(self, j):
        jump_table = {
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }
        if j in jump_table:
            return jump_table[j]
        return '000'


class SymbolTable():
    pre_define_table = {
        'R0': '0',
        'R1': '1',
        'R2': '2',
        'R3': '3',
        'R4': '4',
        'R5': '5',
        'R6': '6',
        'R7': '7',
        'R8': '8',
        'R9': '9',
        'R10': '10',
        'R11': '11',
        'R12': '12',
        'R13': '13',
        'R14': '14',
        'R15': '15',
        'SP' : '0',
        'LCL': '1',
        'ARG': '2',
        'THIS': '3',
        'THAT': '4',
        'KBD': '24576',
        'SCREEN': '16384'
    }

    def __init__(self, lines):
        self.symbol_table = {} | self.pre_define_table
        self.clean_table = {}
        self.clean_lines = []
        self.build_clean_table(lines)
        self.update_symbol_table_label()
        self.update_symbol_table_variable()

    def build_clean_table(self, lines):
        idx = 0
        for line in lines:
            line_clean = line.split('//')[0].strip()
            if not line_clean:
                continue
            self.clean_lines.append(line_clean)
            idx += 1

    def update_symbol_table_label(self):
        idx = 0
        for line in self.clean_lines:
            # Label
            if '(' in line:
                label = line.lstrip('(').rstrip(')')
                if label not in self.symbol_table:
                    self.symbol_table[label] = idx
            else:
                idx += 1

    def update_symbol_table_variable(self):
        # Variable
        var_idx = 16
        for line in self.clean_lines:
            if '@' in line:
                label = line.lstrip('@')
                if label.isdigit():
                    continue
                elif label not in self.symbol_table:
                    self.symbol_table[label] = var_idx
                    var_idx += 1

    def get_symbol_table(self):
        return self.symbol_table


def main():
    filename = sys.argv[1] # e.g. Xxx.asm
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    symbol_table = SymbolTable(lines).get_symbol_table()

    hack_lines = []
    for line in lines:
        parser = Parser(line, symbol_table)
        if parser.type == 'A':
            a_instruction = parser.parse()
            hack_lines.append(a_instruction)
        if parser.type == 'C':
            parser.parse()
            c = parser.comp()
            d = parser.dest()
            j = parser.jump()

            code = Code()
            cc = code.comp(c)
            dd = code.dest(d)
            jj = code.jump(j)

            hack_lines.append('111' + cc + dd + jj)

    hack_filename = filename.split('.')[0] + '.hack'
    with open(hack_filename, 'w') as f:
        f.write('\n'.join(hack_lines))

if __name__ == "__main__":
    main()
