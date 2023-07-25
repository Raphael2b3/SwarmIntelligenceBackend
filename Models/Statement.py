class Statement:
    statement: str
    arguments: list
    agreed: list
    disagreed: list
    misunderstand: list

    def trustMeter(self):
        b = (len(self.agreed) + len(self.disagreed))
        a = 0
        for agreed in self.agreed:
            a += agreed.trustMeter()
        if b == 0: return 0.5
        return a / b

    def misunderstandMeter(self):
        a = len(self.misunderstand)
        b = (len(self.agreed) + len(self.disagreed) + a)
        return a / b

    def totalTrustMeter(self):  # [+++++xxxxx--]
        misunderstand = self.misunderstandMeter()
        understand = 1 - misunderstand
        trustable = self.trustMeter()
        return understand * trustable, understand * (1 - trustable), misunderstand
