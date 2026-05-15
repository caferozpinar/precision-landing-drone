class test():
    def do():
        print("just do")

    class inner():
        def __init__(self,number):
            self.number = number
            print("initalized")
        
        def jd(self):
            print("just do it" + str(self.number))



obj = test.inner(2214)

obj.jd()

obj = test.inner(2213)

obj.jd()