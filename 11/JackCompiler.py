import glob
import os
import sys

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


def compileFile(input_path):
    tokenizer = JackTokenizer(file=input_path)
    tokenizer.tokenize()

    output_path = os.path.splitext(input_path)[0] + '.vm'
    engine = CompilationEngine(tokenizer, output_path)
    engine.compileClass()
    engine.writeVm()
    return output_path


# python JackCompiler.py Seven
# python JackCompiler.py Seven/Main.jack
if __name__ == '__main__':
    input_path = sys.argv[1]

    if os.path.isfile(input_path) and input_path.endswith('.jack'):
        compileFile(input_path)
    elif os.path.isdir(input_path):
        for filename in sorted(glob.glob(os.path.join(input_path, '*.jack'))):
            compileFile(filename)
    else:
        raise ValueError(f'Invalid input path: {input_path}')
