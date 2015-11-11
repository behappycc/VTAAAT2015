import random

class TestCaseGenerator:
    def getTestInput(self, task):
        pass

class Monkey(TestCaseGenerator):
    def __init__(self):
        pass

    def getTestInput(self, clickableButtonList):
        if len(clickableButtonList) > 0:      
            return random.choice(clickableButtonList)
        else:
            return 'empty'

if __name__ == '__main__':
    x = Monkey()
    x.getTestInput(123)