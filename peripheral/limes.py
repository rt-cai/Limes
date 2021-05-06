def Get(sampleID):
    return LimesData(sampleID)

class LimesData:
    def __init__(self, name):
        self.Reads = "(Reads for: %s)" % name
        self.Lineage = ""
        self.etc = ""
        self.Name = name
    
    def Update(self, x):
        self.x = x