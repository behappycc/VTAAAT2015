import CalcImage as calc

class StateImg:
    def __init__(self):
        self.ID = -1
        self.parent = -1


class AutomataImg:
    def __init__(self):
        self.initialState = None
        self.states = []
        self.edges = []

    def main(self):
        calc.pixelCompare('0.png', '123.png')

if __name__ == '__main__':
    x = AutomataImg()
    x.main()