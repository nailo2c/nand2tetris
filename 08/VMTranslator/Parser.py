


class Parser:
    def __init__(self):
        pass

    def clean(self, line):
        return line.split('//')[0].strip()

    def parse(self, line):
        cmd, arg1, arg2 = '', '', ''

        line_split = line.split()
        cmd = line_split[0]
        if len(line_split) == 1:
            pass
        elif cmd == 'label':
            arg1 = line_split[1]
        elif cmd == 'goto':
            arg1 = line_split[1]
        elif cmd == 'if-goto':
            arg1 = line_split[1]
        elif cmd == 'function':
            arg1 = line_split[1]
            arg2 = line_split[2]
        elif cmd == 'call':
            arg1 = line_split[1]
            arg2 = line_split[2]
        elif cmd == 'return':
            pass
        else:
            arg1 = line_split[1]
            arg2 = line_split[2]

        return cmd, arg1, arg2
