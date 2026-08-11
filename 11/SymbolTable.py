

class SymbolTable:
    def __init__(self):
        self.class_table = {}
        self.class_counts = {'STATIC': 0, 'FIELD': 0}

    def startSubroutine(self):
        self.sub_table = {}
        self.sub_counts = {'ARG': 0, 'VAR': 0}

    def define(self, name, type, kind):
        if kind in ['STATIC', 'FIELD']:
            self.class_counts[kind] += 1

            d = {
                'type': type,
                'kind': kind,
                'index': self.class_counts[kind] - 1
            }
            self.class_table[name] = d
        elif kind in ['ARG', 'VAR']:
            self.sub_counts[kind] += 1
            
            d = {
                'type': type,
                'kind': kind,
                'index': self.sub_counts[kind] - 1
            }
            self.sub_table[name] = d
        else:
            pass

    def varCount(self, kind):
        if kind in self.sub_counts:
            return self.sub_counts.get(kind, None)    
        return self.class_counts.get(kind, None)

    def kindOf(self, name):
        if name in self.sub_table:
            return self.sub_table.get(name, {}).get('kind')    
        return self.class_table.get(name, {}).get('kind')

    def typeOf(self, name):
        if name in self.sub_table:
            return self.sub_table.get(name, {}).get('type')    
        return self.class_table.get(name, {}).get('type')

    def indexOf(self, name):
        if name in self.sub_table:
            return self.sub_table.get(name, {}).get('index')   
        return self.class_table.get(name, {}).get('index')


if __name__ == '__main__':
    st = SymbolTable()

    # class scope
    st.define('x', 'int', 'FIELD')
    st.define('y', 'int', 'FIELD')
    st.define('count', 'int', 'STATIC')

    # 進入第一個 method: move(int dx, int dy)
    st.startSubroutine()
    st.define('dx', 'int', 'ARG')
    st.define('dy', 'int', 'ARG')
    st.define('temp', 'int', 'VAR')

    print(st.kindOf('x'))     # 預期: FIELD   ← class scope 還在
    print(st.kindOf('dx'))    # 預期: ARG
    print(st.indexOf('dx'))   # 預期: 0
    print(st.indexOf('dy'))   # 預期: 1
    print(st.varCount('VAR')) # 預期: 1

    # 進入第二個 method: setX(int x)  ← 參數跟 field 同名
    st.startSubroutine()
    st.define('x', 'int', 'ARG')

    print(st.kindOf('x'))     # 預期: ARG  ← subroutine scope 的 x 蓋過 class scope 的 x
    print(st.indexOf('x'))    # 預期: 0    ← 新 method 的 argument index 重新從 0 開始
    print(st.varCount('ARG')) # 預期: 1    ← 上一個 method 的 dx/dy 已經被清空，不算進來
    print(st.kindOf('y'))     # 預期: FIELD ← y 沒被遮蔽，還是查得到 class scope
    print(st.varCount('VAR')) # 預期: 0    ← temp 也被清空了
