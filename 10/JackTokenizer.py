import sys


class JackTokenizer:
    KEYWORD = [
        'class', 'constructor', 'function', 'method', 'field', 'static',
        'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
        'this', 'let', 'do', 'if', 'else', 'while', 'return',
    ]
    SYMBOL = [
        '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
        '&', '|', '<', '>', '=', '~',
    ]
    SYMBOL_MAPPING = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
    }
    INTEGERCONSTANT = [
        i for i in range(0, 32768)
    ]
    STRINGCONSTANT = [

    ]
    IDENTIFIER = []

    def __init__(self, file):
        self.file = file
        self.lines = []
        self.clean()

    def clean(self):
        with open(self.file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        lines = [line.split('//')[0].strip() for line in lines]
        lines = [line.split('/**')[0].strip() for line in lines]
        lines = [line for line in lines if line]
        self.lines = lines
        # lines = [line.split(' ') for line in lines if line]
        # tokens = [token for line in lines for token in line]
        # print(tokens)

    def hasMoreTokens(self):
        while len(self.lines) > 0:
            line = self.lines.pop(0)
            self.advance(line)

    def advance(self, line):
        start_idx = 0
        for i, c in enumerate(line):
            if c == ' ':
                token = line[start_idx:i]
                token_type = self.tokenType(token)
                self.writeXml(token_type)
                start_idx = i + 1
            elif c == '"':
                pass
            elif c in self.SYMBOL:
                pass
            else:
                pass


    def tokenType(self, token):
        if token in self.KEYWORD:
            return f'<keyword> {token} </keyword>'
        elif token in self.SYMBOL:
            if token in self.SYMBOL_MAPPING:
                token = self.SYMBOL_MAPPING[token]
            return f'<symbol> {token} </symbol>'
        elif token in self.INTEGERCONSTANT:
            return f'<integerConstant> {token} </integerConstant>'
        elif token in self.STRINGCONSTANT:
            return f'<stringConstant> {token} </stringConstant>'
        elif token in self.IDENTIFIER:
            return f'<identifier> {token} </identifier>'
        
    def writeXml(self, data):
        print(data)
        
    def execute(self):
        self.hasMoreTokens()


# python JackTokenizer.py ArrayTest/Main.jack
if __name__ == '__main__':
    input_path = sys.argv[1]

    JackTokenizer(
        file=input_path
    ).execute()
