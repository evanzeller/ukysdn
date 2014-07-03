import heapq

class PQEntry:
    def __init__(self, value, pathservice):
        self.value = value
        self.pathservice = pathservice

    def __cmp__(self, other):
        return cmp(self.pathservice.dist[self.value], self.pathservice.dist[other.value])

class PathService:
    def __init__(self):
        self.path = []
        self.dist = []
    
    def setIOService(self, io):
        self.io = io

    def setInventoryService(self, inv):
        self.inv = inv

    def dijkstra(self, src, dst):
        self.dist = []
        previous = []
        weight = []
        nodes = inv.getNodes()
        edges = inv.getEdges()
        for node in nodes:
            weight[nodes.index(node)] = []
        
        queue = []
        
        for edge in edges:
            weight[edge["source"]][edge["target"]] = 1
            weight[edge["target"]][edge["source"]] = 1

        self.dist[src] = 0
        for node in nodes:
            if nodes.index(node) != src:
                self.dist[nodes.index(node)] = float('inf')
                previous[nodes.index(node)] = None

            heapq.heappush(queue, PQEntry(nodes.index(node), self))
        
        while queue:
            u = heapq.heappop(queue)
            for node in u["neighbours"]
                alt = self.dist[u] + weight[u][node]
                if alt < dist[node]:
                    dist[node] = alt
                    previous[node] = u
                    heapq.heapify(queue)

        print previous        
        return previous
        
        
                
