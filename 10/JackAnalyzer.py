import glob
import sys
import os

from JackTokenizer import JackTokenizer


# python JackAnalyzer.py ArrayTest/Main.jack
# python JackAnalyzer.py ExpressionLessSquare
if __name__ == '__main__':
    input_path = sys.argv[1]

    if os.path.isfile(input_path) and input_path.endswith('.jack'): # file case
        tokenizer = JackTokenizer(input_path).execute()
    elif os.path.isdir(input_path): # folder case
        filenames = glob.glob(os.path.join(input_path, '*.jack'))
        for filename in filenames:
            tokenizer = JackTokenizer(filename).execute()
    else:
        raise ValueError(f'Invalid input path: {input_path}')
