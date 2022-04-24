
class Foo:
    x = 0
    argsList = []

    def __init__(self, args):
        # member var init goes here
        self.x = 42
        self.argsList = args

    def bar(self):
        print("foo bar")

        for av in self.argsList:
            print(av)

    def windowTest(self):
        rawString = "ETCYDRESSBEATEN"

        searchWindow = rawString[0:5]

        print(searchWindow)

# === Exec Starts Here ===


av = [1, 1, 2, 3, 5, 8]
j = Foo(av)
j.windowTest()
