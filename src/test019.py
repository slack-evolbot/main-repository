from texttable import Texttable
 
table = Texttable()

table.set_deco(Texttable.HEADER)
table.set_cols_align(["l", "r", "c"])
table.set_cols_width([15, 15, 15])
table.header(['sono1', 'sono2', 'sono3'])
table.add_rows([
        [1, 'aaaaa bbbbb', 'hoge'],
        [2, 'bbb cccc', 'fuga'],
        [3, 'dddd eeee', 'awawa'],
        ], False)

print(table.draw())
