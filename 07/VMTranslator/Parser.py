


class Parser:
    def __init__(self):
        pass

    def clean(self, line):
        return line.split('//')[0].strip()

    def parse(self, line):
        cmd, arg1, arg2 = '', '', ''

        line_split = line.split()
        if len(line_split) == 1:
            cmd = line_split[0]
        elif len(line_split) == 3:
            cmd = line_split[0]
            arg1 = line_split[1]
            arg2 = line_split[2]

        return cmd, arg1, arg2
