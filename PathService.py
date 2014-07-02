class PathService:
    def __init__(self):
        self.path = []
    
    def setIOService(self, io):
        self.io = io

    def setInventoryService(self, inv):
        self.inv = inv

    def dijkstra(self, src, dst):
        
