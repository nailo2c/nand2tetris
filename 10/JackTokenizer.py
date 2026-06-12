import sys


class JackTokenizer:
    KEYWORD = {
        'class', 'constructor', 'function', 'method', 'field', 'static',
        'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
        'this', 'let', 'do', 'if', 'else', 'while', 'return',
    }
    SYMBOL = {
        '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
        '&', '|', '<', '>', '=', '~',
    }
    SYMBOL_MAPPING = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
    }

    def __init__(self, file):
        self.file = file
        self.lines = []
        self.clean()

        self.tokens = []
        self.current_index = -1
        self.current_token = None

    def clean(self):
        with open(self.file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        lines = [line.split('//')[0].strip() for line in lines]

        tmp = []
        in_block_comment = False
        for line in lines:
            if '/**' in line and '*/' in line:
                continue
            elif '/**' in line:
                in_block_comment = True
                continue
            elif in_block_comment:
                if '*/' in line:
                    in_block_comment = False
                    continue
                else:
                    continue
            else:
                tmp.append(line)

        lines = [line for line in tmp if line]
        self.lines = lines
        # lines = [line.split(' ') for line in lines if line]
        # tokens = [token for line in lines for token in line]
        # print(tokens)
        # ['class Main {', 'function void main() {', 'var Array a;', 'var int length;', 'var int i, sum;', 
        # 'let length = Keyboard.readInt("HOW MANY NUMBERS? ");', 'let a = Array.new(length);', 'let i = 0;', 
        # 'while (i < length) {', 'let a[i] = Keyboard.readInt("ENTER THE NEXT NUMBER: ");', 'let i = i + 1;', '}', 
        # 'let i = 0;', 'let sum = 0;', 'while (i < length) {', 'let sum = sum + a[i];', 'let i = i + 1;', '}', 
        # 'do Output.printString("THE AVERAGE IS: ");', 'do Output.printInt(sum / length);', 'do Output.println();', 
        # 'return;', '}', '}']
    
    def hasMoreTokens(self):
        return self.current_index + 1 < len(self.tokens)
    
    def advance(self):
        self.current_index += 1
        self.current_token = self.tokens[self.current_index]

    def tokenize(self):
        while len(self.lines) > 0:
            line = self.lines.pop(0)
            self.tokenizeLine(line)

    def tokenizeLine(self, line):
        in_string = False
        start_idx = 0
        for i, c in enumerate(line):
            if in_string:
                if c != '"':
                    continue
                else:
                    pass

            if c in self.SYMBOL:
                # handle token before the symbol
                if start_idx != i:
                    token = line[start_idx:i]
                    self.tokens.append(token)

                # handle symbol
                token = line[i:i+1]
                self.tokens.append(token)
                start_idx = i + 1
            elif c == ' ':
                if start_idx < i:
                    token = line[start_idx:i]
                    self.tokens.append(token)
                    start_idx = i + 1
                elif start_idx == i:
                    start_idx = i + 1
            elif c == '"':
                if in_string:
                    in_string = False
                    token = line[start_idx:i+1]
                    self.tokens.append(f'{token}')
                    start_idx = i + 1
                else:
                    in_string = True
                    start_idx = i
            else:
                pass

    def tokenType(self):
        if self.current_token in self.KEYWORD:
            return 'keyword'
        elif self.current_token in self.SYMBOL:
            return 'symbol'
        elif self.current_token.startswith('"') and self.current_token.endswith('"'):
            return 'stringConstant'
        elif self.current_token.isdigit():
            return 'integerConstant'
        else:
            return 'identifier'
        
    def formatTokenXml(self):
        token = self.current_token
        token_type = self.tokenType()
        if token_type == 'keyword':
            return f'<keyword> {token} </keyword>'
        elif token_type == 'symbol':
            return f'<symbol> {self.SYMBOL_MAPPING.get(token, token)} </symbol>'
        elif token_type == 'stringConstant':
            return f'<stringConstant> {token[1:-1]} </stringConstant>'
        elif token_type == 'integerConstant':
            return f'<integerConstant> {token} </integerConstant>'
        elif token_type == 'identifier':
            return f'<identifier> {token} </identifier>'
        else:
            raise ValueError('Unexpected Format')
        
    def writeXml(self, data):
        output_path = self.file.split('.')[0] + 'T2.xml'
        with open(output_path, 'w') as f:
            f.write('\n'.join(data) + '\n')
        
    def execute(self):
        self.tokenize()

        output = []
        output.append('<tokens>')

        while self.hasMoreTokens():
            self.advance()
            output.append(self.formatTokenXml())

        output.append('</tokens>')

        self.writeXml(output)


# python JackTokenizer.py ArrayTest/Main.jack
# python JackTokenizer.py ExpressionLessSquare/Main.jack
# python JackTokenizer.py ExpressionLessSquare/Square.jack
# python JackTokenizer.py ExpressionLessSquare/SquareGame.jack
# python JackTokenizer.py Square/Main.jack
# python JackTokenizer.py Square/Square.jack
# python JackTokenizer.py Square/SquareGame.jack
if __name__ == '__main__':
    input_path = sys.argv[1]

    JackTokenizer(
        file=input_path
    ).execute()
