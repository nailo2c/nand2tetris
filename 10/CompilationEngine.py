import sys
from JackTokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self, tokenizer, output_path):
        self.tokenizer = tokenizer
        self.output_path = output_path

        self.indent = ' ' * 2
        self.indent_depth = 0

        self.output = []

    def compileClassVarDec(self):
        self.openTag('classVarDec')
        self.eat()  # eat field
        self.eat()  # eat type
        self.eat()  # eat first var
        while self.peek() == ',':
            self.eat()  # eat comma
            self.eat()  # eat second var
        self.eat()  # eat ;
        self.closeTag('classVarDec')

    def compileSubroutine(self):
        self.openTag('subroutineDec')
        self.eat()  # eat constructor/function/method
        self.eat()  # eat type
        self.eat()  # eat name
        self.eat()  # eat (
        self.compileParameterList()
        self.eat()  # eat )
        self.compileSubroutineBody()
        self.closeTag('subroutineDec')

    def compileParameterList(self):
        self.openTag('parameterList')
        while self.peek() != ')':
            self.eat()
        self.closeTag('parameterList')

    def compileSubroutineBody(self):
        self.openTag('subroutineBody')
        self.eat()  # eat {
        while self.peek() == 'var':
            self.compileVarDec()
        self.compileStatements()
        self.eat()  # eat }
        self.closeTag('subroutineBody')

    def compileVarDec(self):
        self.openTag('varDec')
        self.eat()
        self.eat()
        self.eat()
        while self.peek() == ',':
            self.eat()  # eat comma
            self.eat()  # eat varName
        self.eat()
        self.closeTag('varDec')

    def compileStatements(self):
        self.openTag('statements')
        while self.peek() in ['let', 'if', 'while', 'do', 'return']:
            if self.peek() == 'let':
                self.compileLet()
            elif self.peek() == 'while':
                self.compileWhile()
            elif self.peek() == 'do':
                self.compileDo()
            elif self.peek() == 'return':
                self.compileReturn()
            elif self.peek() == 'if':
                self.compileIf()
        self.closeTag('statements')

    def compileDo(self):
        self.openTag('doStatement')
        self.eat()  # eat do
        self.eat()  # eat first identifier
        while self.peek() == '.':
            self.eat()  # eat .
            self.eat()  # eat print function
        self.eat()  # eat (
        self.compileExpressionList()
        self.eat()  # eat )

        self.eat()  # eat ;
        self.closeTag('doStatement')

    def compileLet(self):
        self.openTag('letStatement')
        self.eat()  # eat let
        self.eat()  # eat varName

        while self.peek() == '[':
            self.eat()  # eat [
            self.compileExpression()
            self.eat()  # eat ]
        while self.peek() == '=':
            self.eat()  # eat =
            self.compileExpression()
            self.eat()  # eat ;

        self.closeTag('letStatement')

    def compileWhile(self):
        self.openTag('whileStatement')
        self.eat()  # eat while
        self.eat()  # eat (
        self.compileExpression()
        self.eat()  # eat )
        self.eat()  # eat {
        self.compileStatements()
        self.eat()  # eat }
        self.closeTag('whileStatement')

    def compileReturn(self):
        self.openTag('returnStatement')
        self.eat()  # eat return
        if self.peek() != ';':
            self.compileExpression()
        self.eat()  # eat ;
        self.closeTag('returnStatement')

    def compileIf(self):
        self.openTag('ifStatement')
        self.eat()  # eat if
        self.eat()  # eat (
        self.compileExpression()
        self.eat()  # eat )
        self.eat()  # eat {
        self.compileStatements()
        self.eat()  # eat }

        if self.peek() == 'else':
            self.eat()  # eat else
            self.eat()  # eat {
            self.compileStatements()
            self.eat()  # eat }

        self.closeTag('ifStatement')

    def compileExpression(self):
        self.openTag('expression')
        self.compileTerm()
        while self.peek() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.eat()  # eat operator
            self.compileTerm()
        self.closeTag('expression')
        # while self.peek() == ',':
        #     self.eat()  # eat ,

    def compileTerm(self):
        self.openTag('term')

        if self.peek() == '(':
            self.eat()  # eat (
            self.compileExpression()
            self.eat()  # eat )
        elif self.peek() in ['-', '~']:
            self.eat()  # eat - or ~
            self.compileTerm()
        else:
            self.eat()
            while self.peek() == '.':
                self.eat()  # eat .
                self.eat()  # eat attribute
            while self.peek() == '(':
                self.eat()  # eat (
                self.compileExpressionList()
                self.eat()  # eat )
            while self.peek() == '[':
                self.eat()  # eat [
                self.compileExpression()
                self.eat()  # eat ]

        self.closeTag('term')

    def compileExpressionList(self):
        self.openTag('expressionList')
        if self.peek() != ')':
            self.compileExpression()
        while self.peek() == ',':
            self.eat()
            self.compileExpression()
        self.closeTag('expressionList')

    def test_print(self, data):
        print(self.indent * self.indent_depth + data)

    def emit(self, line):
        indent_line = self.indent * self.indent_depth + line
        # self.test_print(indent_line)
        print(indent_line)
        self.output.append(indent_line)

    def openTag(self, tag):
        self.emit(f'<{tag}>')
        self.indent_depth += 1

    def closeTag(self, tag):
        self.indent_depth -= 1
        self.emit(f'</{tag}>')

    def eat(self):
        self.tokenizer.advance()
        self.emit(self.tokenizer.formatTokenXml())

    def peek(self):
        return self.tokenizer.tokens[self.tokenizer.current_index + 1]

    def writeXml(self):
        with open(self.output_path, 'w') as f:
            f.write('\n'.join(self.output) + '\n')

    def compileClass(self):

        self.openTag('class')
        self.eat()  # eat class
        self.eat()  # eat Main
        self.eat()  # eat {
        while self.peek() in ['field', 'static']:
            self.compileClassVarDec()
        while self.peek() in ['constructor', 'function', 'method']:
            self.compileSubroutine()
        self.eat()  # eat }
        self.closeTag('class')

        self.writeXml()


# python CompilationEngine.py ArrayTest/Main.jack
# python CompilationEngine.py ExpressionLessSquare/Square.jack
# python CompilationEngine.py ExpressionLessSquare/Main.jack
# python CompilationEngine.py ExpressionLessSquare/SquareGame.jack
# python CompilationEngine.py Square/Main.jack
# python CompilationEngine.py Square/Square.jack
# python CompilationEngine.py Square/SquareGame.jack
if __name__ == '__main__':
    input_path = sys.argv[1]

    tokenizer = JackTokenizer(file=input_path)
    tokenizer.tokenize()

    # print(tokenizer.tokens)

    output_path = input_path.split('.')[0] + '.xml'
    # print(output_path)

    engine = CompilationEngine(tokenizer, output_path)
    engine.compileClass()
