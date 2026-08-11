import os
import sys
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    ARITH_MAP = {
        '+': 'add', '-': 'sub', '&': 'and', '|': 'or',
        '<': 'lt', '>': 'gt', '=': 'eq',
    }

    SEGMENT_MAP = {'VAR': 'local', 'ARG': 'argument', 'FIELD': 'this', 'STATIC': 'static'}

    def __init__(self, tokenizer, output_path):
        self.tokenizer = tokenizer
        self.output_path = output_path

        self.indent = ' ' * 2
        self.indent_depth = 0

        self.output = []

        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter()

        self.label_count = 0

    def compileClassVarDec(self):
        self.openTag('classVarDec')
        kind = self.eat().upper()  # eat field -> FIELD
        var_type = self.eat()  # eat type
        name = self.eat()  # eat first var
        self.symbol_table.define(name, var_type, kind)
        while self.peek() == ',':
            self.eat()  # eat comma
            name = self.eat()  # eat second var
            self.symbol_table.define(name, var_type, kind)
        self.eat()  # eat ;
        self.closeTag('classVarDec')

    def compileSubroutine(self):
        self.openTag('subroutineDec')
        sub_kind = self.eat()  # eat constructor/function/method
        self.eat()  # eat type
        sub_name = self.eat()  # eat name
        self.symbol_table.startSubroutine()
        if sub_kind == 'method':
            self.symbol_table.define('this', self.class_name, 'ARG')
        self.eat()  # eat (
        self.compileParameterList()
        self.eat()  # eat )
        self.compileSubroutineBody(sub_name, sub_kind)
        self.closeTag('subroutineDec')

    def compileParameterList(self):
        self.openTag('parameterList')
        if self.peek() != ')':
            var_type = self.eat()
            name = self.eat()
            self.symbol_table.define(name, var_type, 'ARG')
            while self.peek() == ',':
                self.eat()  # eat comma
                var_type = self.eat()
                name = self.eat()
                self.symbol_table.define(name, var_type, 'ARG')
        self.closeTag('parameterList')

    def compileSubroutineBody(self, sub_name, sub_kind):
        self.openTag('subroutineBody')
        self.eat()  # eat {
        while self.peek() == 'var':
            self.compileVarDec()
        n_locals = self.symbol_table.varCount('VAR')
        self.vm_writer.writeFunction(f'{self.class_name}.{sub_name}', n_locals)

        if sub_kind == 'method':
            self.vm_writer.writePush('argument', 0)
            self.vm_writer.writePop('pointer', 0)
        elif sub_kind == 'constructor':
            n_fields = self.symbol_table.varCount('FIELD')
            self.vm_writer.writePush('constant', n_fields)
            self.vm_writer.writeCall('Memory.alloc', 1)
            self.vm_writer.writePop('pointer', 0)

        self.compileStatements()
        self.eat()  # eat }
        self.closeTag('subroutineBody')

    def compileVarDec(self):
        self.openTag('varDec')
        self.eat()
        var_type = self.eat()
        name = self.eat()
        self.symbol_table.define(name, var_type, 'VAR')
        while self.peek() == ',':
            self.eat()  # eat comma
            name = self.eat()  # eat varName
            self.symbol_table.define(name, var_type, 'VAR')
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

    def compileSubroutineCall(self, first_name):
        kind = self.symbol_table.kindOf(first_name)

        if self.peek() == '.':
            self.eat()  # eat .
            second_name = self.eat()  # eat subroutine name
            if kind is not None:
                # first_name is a variable -> method call: push it as the implicit this
                var_type = self.symbol_table.typeOf(first_name)
                segment = self.SEGMENT_MAP[kind]
                index = self.symbol_table.indexOf(first_name)
                self.vm_writer.writePush(segment, index)
                call_name = f'{var_type}.{second_name}'
                n_args_extra = 1
            else:
                # first_name is a class name -> function/constructor call
                call_name = f'{first_name}.{second_name}'
                n_args_extra = 0
        else:
            # bare call: method of the current class -> push this
            self.vm_writer.writePush('pointer', 0)
            call_name = f'{self.class_name}.{first_name}'
            n_args_extra = 1

        self.eat()  # eat (
        n_args = self.compileExpressionList()
        self.eat()  # eat )
        self.vm_writer.writeCall(call_name, n_args + n_args_extra)

    def compileDo(self):
        self.openTag('doStatement')
        self.eat()  # eat do
        first_name = self.eat()  # eat first identifier
        self.compileSubroutineCall(first_name)
        self.vm_writer.writePop('temp', 0)
        self.eat()  # eat ;
        self.closeTag('doStatement')

    def compileLet(self):
        self.openTag('letStatement')
        self.eat()  # eat let
        name = self.eat()  # eat varName

        is_array = self.peek() == '['
        if is_array:
            kind = self.symbol_table.kindOf(name)
            index = self.symbol_table.indexOf(name)
            self.vm_writer.writePush(self.SEGMENT_MAP[kind], index)
            self.eat()  # eat [
            self.compileExpression()
            self.eat()  # eat ]
            self.vm_writer.writeArithmetic('add')  # arr + index

        self.eat()  # eat =
        self.compileExpression()

        if is_array:
            self.vm_writer.writePop('temp', 0)
            self.vm_writer.writePop('pointer', 1)
            self.vm_writer.writePush('temp', 0)
            self.vm_writer.writePop('that', 0)
        else:
            kind = self.symbol_table.kindOf(name)
            index = self.symbol_table.indexOf(name)
            self.vm_writer.writePop(self.SEGMENT_MAP[kind], index)

        self.eat()  # eat ;
        self.closeTag('letStatement')

    def compileWhile(self):
        self.openTag('whileStatement')
        label_id = self.label_count
        self.label_count += 1
        start_label = f'WHILE_EXP{label_id}'
        end_label = f'WHILE_END{label_id}'

        self.eat()  # eat while
        self.eat()  # eat (
        self.vm_writer.writeLabel(start_label)
        self.compileExpression()
        self.vm_writer.writeArithmetic('not')
        self.vm_writer.writeIf(end_label)
        self.eat()  # eat )
        self.eat()  # eat {
        self.compileStatements()
        self.vm_writer.writeGoto(start_label)
        self.vm_writer.writeLabel(end_label)
        self.eat()  # eat }
        self.closeTag('whileStatement')

    def compileReturn(self):
        self.openTag('returnStatement')
        self.eat()  # eat return
        if self.peek() != ';':
            self.compileExpression()
        else:
            self.vm_writer.writePush('constant', 0)
        self.eat()  # eat ;
        self.vm_writer.writeReturn()
        self.closeTag('returnStatement')

    def compileIf(self):
        self.openTag('ifStatement')
        label_id = self.label_count
        self.label_count += 1
        false_label = f'IF_FALSE{label_id}'
        end_label = f'IF_END{label_id}'

        self.eat()  # eat if
        self.eat()  # eat (
        self.compileExpression()
        self.eat()  # eat )

        self.vm_writer.writeArithmetic('not')
        self.vm_writer.writeIf(false_label)

        self.eat()  # eat {
        self.compileStatements()
        self.eat()  # eat }

        if self.peek() == 'else':
            self.vm_writer.writeGoto(end_label)
            self.vm_writer.writeLabel(false_label)
            self.eat()  # eat else
            self.eat()  # eat {
            self.compileStatements()
            self.eat()  # eat }
            self.vm_writer.writeLabel(end_label)
        else:
            self.vm_writer.writeLabel(false_label)

        self.closeTag('ifStatement')

    def compileExpression(self):
        self.openTag('expression')
        self.compileTerm()
        while self.peek() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            op = self.eat()  # eat operator
            self.compileTerm()
            if op == '*':
                self.vm_writer.writeCall('Math.multiply', 2)
            elif op == '/':
                self.vm_writer.writeCall('Math.divide', 2)
            else:
                self.vm_writer.writeArithmetic(self.ARITH_MAP[op])
        self.closeTag('expression')

    def compileTerm(self):
        self.openTag('term')

        if self.peek() == '(':
            self.eat()  # eat (
            self.compileExpression()
            self.eat()  # eat )
        elif self.peek() in ['-', '~']:
            op = self.eat()  # eat - or ~
            self.compileTerm()
            if op == '-':
                self.vm_writer.writeArithmetic('neg')
            elif op == '~':
                self.vm_writer.writeArithmetic('not')
        else:
            token = self.eat()
            token_type = self.tokenizer.tokenType()

            if self.tokenizer.tokenType() == 'integerConstant':
                self.vm_writer.writePush('constant', token)
            elif token_type == 'keyword':
                if token == 'true':
                    self.vm_writer.writePush('constant', 0)
                    self.vm_writer.writeArithmetic('not')
                elif token == 'false':
                    self.vm_writer.writePush('constant', 0)
                elif token == 'this':
                    self.vm_writer.writePush('pointer', 0)
                elif token == 'null':
                    self.vm_writer.writePush('constant', 0)
            elif token_type == 'identifier':
                if self.peek() in ['.', '(']:
                    self.compileSubroutineCall(token)
                elif self.peek() == '[':
                    kind = self.symbol_table.kindOf(token)
                    index = self.symbol_table.indexOf(token)
                    self.vm_writer.writePush(self.SEGMENT_MAP[kind], index)
                    self.eat()  # eat [
                    self.compileExpression()  # push index
                    self.eat()  # eat ]
                    self.vm_writer.writeArithmetic('add')
                    self.vm_writer.writePop('pointer', 1)
                    self.vm_writer.writePush('that', 0)
                else:
                    kind = self.symbol_table.kindOf(token)
                    index = self.symbol_table.indexOf(token)
                    self.vm_writer.writePush(self.SEGMENT_MAP[kind], index)
            elif token_type == 'stringConstant':
                string_value = token[1:-1]  # strip surrounding quotes
                self.vm_writer.writePush('constant', len(string_value))
                self.vm_writer.writeCall('String.new', 1)
                for c in string_value:
                    self.vm_writer.writePush('constant', ord(c))
                    self.vm_writer.writeCall('String.appendChar', 2)

        self.closeTag('term')

    def compileExpressionList(self):
        self.openTag('expressionList')
        n_args = 0
        if self.peek() != ')':
            self.compileExpression()
            n_args += 1
        while self.peek() == ',':
            self.eat()
            self.compileExpression()
            n_args += 1
        self.closeTag('expressionList')
        return n_args

    def test_print(self, data):
        print(self.indent * self.indent_depth + data)

    def emit(self, line):
        indent_line = self.indent * self.indent_depth + line
        # self.test_print(indent_line)
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
        return self.tokenizer.current_token

    def peek(self):
        return self.tokenizer.tokens[self.tokenizer.current_index + 1]

    def writeXml(self):
        with open(self.output_path, 'w') as f:
            f.write('\n'.join(self.output) + '\n')

    def writeVm(self):
        with open(self.output_path, 'w') as f:
            f.write('\n'.join(self.vm_writer.output) + '\n')

    def compileClass(self):
        self.openTag('class')
        self.eat()  # eat class
        self.class_name = self.eat()  # eat Main
        self.eat()  # eat {
        while self.peek() in ['field', 'static']:
            self.compileClassVarDec()
        while self.peek() in ['constructor', 'function', 'method']:
            self.compileSubroutine()
        self.eat()  # eat }
        self.closeTag('class')

# python CompilationEngine.py Average/Main.jack
# python CompilationEngine.py Seven/Main.jack
# python CompilationEngine.py ConvertToBin/Main.jack
# python CompilationEngine.py Square/Main.jack
# python CompilationEngine.py Square/Square.jack
# python CompilationEngine.py Square/SquareGame.jack
if __name__ == '__main__':
    input_path = sys.argv[1]

    tokenizer = JackTokenizer(file=input_path)
    tokenizer.tokenize()

    # print(tokenizer.tokens)

    output_path = os.path.splitext(input_path)[0] + '.vm'
    # print(output_path)

    engine = CompilationEngine(tokenizer, output_path)
    engine.compileClass()
    engine.writeVm()

    # print(engine.symbol_table.class_table)
    # print(engine.symbol_table.sub_table)
    # print(engine.vm_writer.output)
