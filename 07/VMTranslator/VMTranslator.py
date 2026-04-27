import sys
from CodeWriter import CodeWriter
from Parser import Parser

def main():
    # read .vm file
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    p = Parser()
    c = CodeWriter(filename)

    for line in lines:
        line_clean = p.clean(line)
        if not line_clean:
            continue
        # e.g. cmd=push, arg1=constant arg2=7
        cmd, arg1, arg2 = p.parse(line_clean)

        c.compile(cmd, arg1, arg2)

    asm_lines = c.compile_lines  # ['@7', 'D=A', '@SP', 'A=M', ...]

    # write .asm file
    asm_filename = filename.split('.')[0] + '.asm'
    with open(asm_filename, 'w') as f:
        f.write('\n'.join(asm_lines))

# usage : python VMTranslator/VMTranslator.py MemoryAccess/BasicTest/BasicTest.vm
# varify: ./verify.sh
if __name__ == '__main__':
    main()
