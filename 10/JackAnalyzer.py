import glob
import sys
import os

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


# python JackAnalyzer.py ArrayTest/Main.jack
# python JackAnalyzer.py ExpressionLessSquare
if __name__ == '__main__':
    input_path = sys.argv[1]

    if os.path.isfile(input_path) and input_path.endswith('.jack'): # file case
        tokenizer = JackTokenizer(file=input_path)
        tokenizer.tokenize()
        output_path = input_path.split('.')[0] + '.xml'
        engine = CompilationEngine(tokenizer, output_path)
        engine.compileClass()
    elif os.path.isdir(input_path): # folder case
        filenames = glob.glob(os.path.join(input_path, '*.jack'))
        for filename in filenames:
            tokenizer = JackTokenizer(file=filename)
            tokenizer.tokenize()
            output_path = filename.split('.')[0] + '.xml'
            engine = CompilationEngine(tokenizer, output_path)
            engine.compileClass()
    else:
        raise ValueError(f'Invalid input path: {input_path}')
