import os

class CodeWriter:
    def __init__(self, filename):
        self.compile_lines = []

        base_name = os.path.basename(filename)
        self.filename = base_name.split('.')[0]  # e.g. BasicTest.vm -> BasicTest

        self.jump_cnt = 0
        
        self.ARITHMETRIC_CMDS = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
        self.MEMORY_ACCESS_CMDS = ['push', 'pop']
        self.SEGMENT_MAP = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
        }

    def compile(self, cmd, arg1, arg2):
        if cmd in self.ARITHMETRIC_CMDS:
            self.arithmetric_cmd_handler(cmd)
        elif cmd in self.MEMORY_ACCESS_CMDS:
            self.memory_access_cmd_handler(cmd, arg1, arg2)

        return []

    def arithmetric_cmd_handler(self, cmd):
        # stack = [1, 2, 3], False=0, True=-1
        # add=2+3 / sub=2-3 / neg=-3
        # eq -> 2==3 -> 0 / gt -> 2>3 -> 0 / lt -> 2<3 -> -1
        # 2 and 3 = 010 & 011 = 010 = 2
        # 2 or  3 = 010 or 011 = 011 = 3
        # not 3 = not 011 = 100 = 4
        if cmd in ['add', 'sub', 'and', 'or']:
            if cmd == 'add':
                op = 'M=D+M'
            elif cmd == 'sub':
                op = 'M=M-D'
            elif cmd == 'and':
                op = 'M=D&M'
            elif cmd == 'or':
                op = 'M=D|M'

            self.compile_lines.extend([
                '@SP',   # SP--
                'M=M-1',
                'A=M',
                'D=M',   # e.g. 3
                '@SP',
                'M=M-1', # SP--
                'A=M',
                op, # e.g. 3+2 and write it to the top
                '@SP',
                'M=M+1', # SP++
            ])
        elif cmd in ['eq', 'gt', 'lt']:
            if cmd == 'eq':
                op = 'JEQ'
            elif cmd == 'gt':
                op = 'JGT'
            elif cmd == 'lt':
                op = 'JLT'

            label_true = f'{op}_TRUE_{self.jump_cnt}'
            label_end = f'{op}_END_{self.jump_cnt}'
            self.jump_cnt += 1

            self.compile_lines.extend([
                '@SP',    # SP--
                'M=M-1',
                'A=M',
                'D=M',    # e.g. 3
                '@SP',
                'M=M-1',  # SP--,
                'A=M',
                'D=M-D',  # calculate D=2-3

                # if D==0
                f'@{label_true}',
                f'D;{op}',

                # else D!=0
                '@SP',
                'A=M',
                'M=0',   # False -> write 0
                f'@{label_end}',
                '0;JMP',

                # logic of if
                f'({label_true})',
                '@SP',
                'A=M',
                'M=-1',  # True -> write -1

                # move SP back
                f'({label_end})',
                '@SP',
                'M=M+1',
            ])

        elif cmd in ['not', 'neg']:
            op = '!' if cmd == 'not' else '-'

            # 1. SP--, get data from top of stack
            # 2. calculate not val (by using !)
            # 3. put it back to top of stack, and SP++
            self.compile_lines.extend([
                '@SP',  # SP--
                'M=M-1',
                'A=M',  # get data
                'D=M',
                f'M={op}D',
                '@SP',  # SP+=
                'M=M+1'
            ])

    def memory_access_cmd_handler(self, cmd, arg1, arg2):
        if arg1 in ['local', 'argument', 'this', 'that']:
            self.segment_handler(cmd, arg1, arg2)
        elif arg1 in ['constant']:
            self.constant_handler(cmd, arg1, arg2)
        elif arg1 in ['static']:
            self.static_handler(cmd, arg1, arg2)
        elif arg1 in ['temp']:
            self.temp_handler(cmd, arg1, arg2)
        elif arg1 in ['pointer']:
            self.pointer_handler(cmd, arg1, arg2)

    def segment_handler(self, cmd, arg1, arg2):
        addr = self.SEGMENT_MAP[arg1]
        if cmd == 'push':
            self.compile_lines.extend([
                f'@{arg2}',
                'D=A',       # store arg2 to D
                f'@{addr}',
                'A=D+M',     # arg2 + segment_addr
                'D=M',
                '@SP',
                'A=M',
                'M=D',   # M[SP]=M[addr] <=> *SP=*addr
                '@SP',   # SP++
                'M=M+1',
            ])
        elif cmd == 'pop':
            self.compile_lines.extend([
                # 1. Store address `addr+arg2` to somewhere (we use R13 as temp)
                f'@{arg2}',  # e.g. 2
                'D=A',
                f'@{addr}',  # e.g. LCL
                'D=D+M',     # e.g. D+M[LCL] = 2+300 = 302
                '@R13',
                'M=D',       # e.g. M[R13]=302

                # 2. Stack pop and store it to D
                '@SP',
                'M=M-1',     # point to the top of the stack
                'A=M',       # addr of the top of the stack
                'D=M',       # store the value of the top of the stack to D

                # 3. Write data to `addr+arg2`(take this addr from R13)
                '@R13',
                'A=M',       # A=302
                'M=D',       # M[302]=M[SP] <=> write stack top value to 302
            ])

    def constant_handler(self, cmd, arg1, arg2):
        if cmd == 'push':
            self.compile_lines.extend([
                f'@{arg2}',  # D=i
                'D=A',
                '@SP',       # *SP=D
                'A=M',       # e.g. if M[SP]=256, then A=256
                'M=D',       # M[256] = D <=> *SP = i
                '@SP',
                'M=M+1',
            ])

    def static_handler(self, cmd, arg1, arg2):
        if cmd == 'push':
            self.compile_lines.extend([
                f'@{self.filename}.{arg2}',
                'D=M',   # get value in RAM[@StaticTest.1]
                '@SP',   # Implemented *SP = D
                'A=M',   # A = M[@SP]
                'M=D',
                '@SP',   # SP++
                'M=M+1',  
            ])
        elif cmd == 'pop':
            # SP--  // move pointer to the top of the stack
            # *addr = *SP  // put data to static mem addr
            self.compile_lines.extend([
                '@SP',
                'M=M-1', # e.g. 257 -> 256
                'A=M',   # A=256
                'D=M',   # put RAM[256] data to D
                f'@{self.filename}.{arg2}',
                'M=D',
            ])

    def temp_handler(self, cmd, arg1, arg2):
        addr = 5 + int(arg2)
        if cmd == 'push':
            self.compile_lines.extend([
                f'@{addr}',
                'D=M',
                '@SP',
                'A=M',
                'M=D',
                '@SP',
                'M=M+1'
            ])
        elif cmd == 'pop':
            self.compile_lines.extend([
                '@SP',
                'M=M-1', # point to the top of stack
                'A=M',   # record the addr of top of stack
                'D=M',   # record value of top of stack to D register
                f'@{addr}', 
                'M=D',   # write value of top of stack to temp i
            ])

    def pointer_handler(self, cmd, arg1, arg2):
        if cmd == 'push':
            # *SP=*THIS, SP++
            addr = '@THIS' if arg2 == '0' else '@THAT'
            self.compile_lines.extend([
                addr,
                'D=M',
                '@SP',
                'A=M',
                'M=D',
                '@SP',
                'M=M+1',
            ])
        elif cmd == 'pop':
            # SP--, *THAT=*SP
            addr = '@THIS' if arg2 == '0' else '@THAT'
            self.compile_lines.extend([
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                addr,
                'M=D',
            ])
