import glob
import os
import sys
from CodeWriter import CodeWriter
from Parser import Parser


def translator(p, c, lines):
    for line in lines:
        line_clean = p.clean(line)
        if not line_clean:
            continue
        # e.g. cmd=push, arg1=constant arg2=7
        cmd, arg1, arg2 = p.parse(line_clean)

        c.compile(cmd, arg1, arg2)


def main():
    input_path = sys.argv[1]

    p = Parser()
    c = CodeWriter()

    if os.path.isfile(input_path) and input_path.endswith('.vm'): # file case
        c.booting(mode='file')

        filename = input_path
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        c.set_filename(filename)
        translator(p, c, lines)
        output = os.path.splitext(input_path)[0] + '.asm'
    elif os.path.isdir(input_path): # folder case
        c.booting(mode='folder')

        filenames = glob.glob(os.path.join(input_path, '*.vm'))
        for filename in filenames:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f.readlines()]
            c.set_filename(filename)
            translator(p, c, lines)
        folder_name = os.path.basename(os.path.normpath(input_path))
        output = os.path.join(input_path, folder_name + '.asm')
    else:
        raise ValueError(f'Invalid input path: {input_path}')
    
    with open(output, 'w') as f:
        f.write('\n'.join(c.compile_lines))
        

# usage : python VMTranslator/VMTranslator.py FunctionCalls/StaticsTest
# varify: ./verify.sh
if __name__ == '__main__':
    main()
