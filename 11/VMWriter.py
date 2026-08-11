
class VMWriter:
    def __init__(self):
        self.output = []

    def writePush(self, segment, index):
        self.output.append(f'push {segment} {index}')

    def writePop(self, segment, index):
        self.output.append(f'pop {segment} {index}')

    def writeArithmetic(self, command):
        self.output.append(command)

    def writeLabel(self, label):
        self.output.append(f'label {label}')

    def writeGoto(self, label):
        self.output.append(f'goto {label}')

    def writeIf(self, label):
        self.output.append(f'if-goto {label}')

    def writeCall(self, name, nArgs):
        self.output.append(f'call {name} {nArgs}')

    def writeFunction(self, name, nLocals):
        self.output.append(f'function {name} {nLocals}')

    def writeReturn(self):
        self.output.append('return')


if __name__ == '__main__':
    vw = VMWriter()
    vw.writePush('local', 0)
    vw.writePush('constant', 1)
    vw.writeArithmetic('add')
    vw.writePop('this', 2)
    vw.writeCall('Math.multiply', 2)
    vw.writeFunction('Square.new', 3)
    vw.writeReturn()

    for line in vw.output:
        print(line)
