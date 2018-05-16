class B():
    AAAA = 'bbbb'

def C():
    C.AAAA = "cccc"


#    FOO = int()
#
#    def get_foo(self):
#        return self.FOO

def D():
    print(C.AAAA)

C()
D()
