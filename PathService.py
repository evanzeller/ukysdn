import heapq

class PQEntry:
    def __init__(self, value, pathservice):
        self.value = value
        self.pathservice = pathservice

    def __cmp__(self, other):
        return cmp(self.pathservice.dist[self.value], self.pathservice.dist[other.value])

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

class PathService:
    def __init__(self):
        self.path = []
        self.dist = []
    
    def setIOService(self, io):
        self.io = io

    def setInventoryService(self, inv):
        self.inv = inv

    def dijkstra(self, src, dst):
        self.dist = {}
        previous = {}
        weight = {}
        nodes = self.inv.getNodes()
        edges = self.inv.getEdges()
        for node in nodes:
            weight[nodes.index(node)] = {}
        
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
            for node in nodes[u.value]["neighbours"]:
                alt = self.dist[u.value] + weight[u.value][node]
                if alt < self.dist[node]:
                    self.dist[node] = alt
                    previous[node] = u.value
                    heapq.heapify(queue)

        currNode = dst
        lastNode = None
        path = {}
        path["srcIp"] = nodes[src]["networkAddress"]
        path["dstIp"] = nodes[dst]["networkAddress"]
        print previous
        while True:
            prev = None
            if currNode != src:
                prev = previous[currNode]
            print prev
            if lastNode == None:
                path[currNode] = {
                    "node":{
                        "type":nodes[currNode]["node"]["type"],
                        "id":nodes[currNode]["node"]["id"]
                    },
                    "next":{
                        "index":prev,
                        "port":nodes[currNode]["neighbours"][prev]
                    },
                    "return":None
                }
            elif prev == None:
                path[currNode] = {
                    "node":{
                        "type":nodes[currNode]["node"]["type"],
                        "id":nodes[currNode]["node"]["id"]
                    },
                    "next":None,
                    "return":{
                        "index":lastNode,
                        "port":nodes[currNode]["neighbours"][lastNode]
                    }
                }
            else:
                path[currNode] = { 
                    "node":{ 
                        "type":nodes[currNode]["node"["type"],
                        "id":nodes[currNode]["node"]["id"]
                    },
                    "next":{
                        "index":prev,
                        "port":nodes[currNode]["neighbours"][prev]
                    },
                    "return":{
                        "index":lastNode,
                        "port":nodes[currNode]["neighbours"][lastNode]
                    }
                }
            lastNode = currNode
            if currNode == src:
                break
            currNode = previous[currNode]
        print path
        return path

    def pushPath(self, path, name):
        for node.key in path:
            if path[node.key]["node"]["type"] == "OF":
                url = "/controller/nb/v2/flowprogrammer/default/node/OF/" + node["node"]["id"] + \
                        "/staticFlow/" + name

                flow = {
                    "installInHw":"true",
                    "name":name,
                    "node":{
                        "id":node["nodeId"],
                        "type":"OF"
                    },
                    "priority":"500",
                    "etherType":"0x0800",
                    "nwSrc":path["srcIp"],
                    "nwDst":path["dstIp"],
                    "actions":[
                        "OUTPUT=" + str(node["next"]["port"])
                    ]
                }
                 
        
        
                
