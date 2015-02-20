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

    def getNodeByIp(self, ip):
        nodes = self.inv.getNodes()
        for node in nodes:
            if node["node"]["type"] == "HOST":
                if node["networkAddress"] == ip:
                    return nodes.index(node)

    def dijkstra(self, src, dst):
        self.dist = {}
        previous = {}
        weight = {}
        nodes = self.inv.getNodes()
        edges = self.inv.getEdges()
        for node in nodes:
            weight[nodes.index(node)] = {}
        
        queue = []
        
        #TODO: weights based on bandwidth reported
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

        currNodeIndex = previous[dst]
        currNode = nodes[currNodeIndex]
        lastNode = None
        path = {}
        path["srcIp"] = nodes[src]["networkAddress"]
        path["dstIp"] = nodes[dst]["networkAddress"]
        while True:
            currNode = nodes[currNodeIndex]
            prev = None
            if currNodeIndex != src:
                prev = previous[currNodeIndex]
            path[currNodeIndex] = {}
            if lastNode == None:
                path[currNodeIndex] = {
                    'node':{
                            "type":currNode["node"]["type"],
                            "id":currNode["node"]["id"],
                    },
                    "next":{
                        "index":prev,
                        "port":currNode["neighbours"][prev],
                    },
                    "return":None,
                }
                path[currNodeIndex]["node"] = { "type":currNode["node"]["type"], "id":currNode["node"]["id"] }
                path[currNodeIndex]["next"] = { "index":prev, "port":currNode["neighbours"][prev] }
            elif prev == None:
                path[currNodeIndex] = {
                    "node":{
                        "type":nodes[currNodeIndex]["node"]["type"],
                        "id":nodes[currNodeIndex]["node"]["id"],
                    },
                    "next":None,
                    "return":{
                        "index":lastNode,
                        "port":nodes[currNodeIndex]["neighbours"][lastNode],
                    },
                }
                path[currNodeIndex]["node"] = { "type":currNode["node"]["type"], "id":currNode["node"]["id"] }
                path[currNodeIndex]["return"] = { "index":lastNode, "port":currNode["neighbours"][lastNode] }
            else:
                path[currNodeIndex] = 
                    {
                        "node":{
                            "type":nodes[currNodeIndex]["node"["type"],
                            "id":nodes[currNodeIndex]["node"]["id"],
                        },
                        "next":{
                            "index":prev,
                            "port":nodes[currNodeIndex]["neighbours"][prev],
                        },
                        "return":{
                            "index":lastNode,
                            "port":nodes[currNodeIndex]["neighbours"][lastNode],
                        },
                    }
                path[currNodeIndex]["node"] = { "type":currNode["node"]["type"], "id":currNode["node"]["id"] }
                path[currNodeIndex]["next"] = { "index":prev, "port":currNode["neighbours"][prev] }
                path[currNodeIndex]["return"] = { "index":lastNode, "port":currNode["neighbours"][lastNode] }
            lastNode = currNodeIndex
            if currNodeIndex == src:
                break
            currNodeIndex = previous[currNodeIndex]
        print path
        return path

    def pushPath(self, name, path):
        for key in path:
            if key != "srcIp" and key != "dstIp":
                node = path[key]
                if node["node"]["type"] == "OF":
                    if "next" in node:
                        url = "/controller/nb/v2/flowprogrammer/default/node/OF/" +\
                                node["node"]["id"] + "/staticFlow/" + name
                        flow = {
                            "installInHw":"true",
                            "vlanId":"162",
                            "name":name,
                            "node":{
                                "id":node["node"]["id"],
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
                        self.io.put(url, flow)

                    if "return" in node:
                        name = name + "_return"
                        url = "/controller/nb/v2/flowprogrammer/default/node/OF/" +\
                                node["node"]["id"] + "/staticFlow/" + name
                        flow = { 
                            "installInHw":"true",
                            "vlanId":"162",
                            "name":name,
                            "node":{
                                "id":node["node"]["id"],
                                "type":"OF"
                            },  
                            "priority":"500",
                            "etherType":"0x0800",
                            "nwSrc":path["dstIp"],
                            "nwDst":path["srcIp"],
                            "actions":[
                                "OUTPUT=" + str(node["return"]["port"])
                            ]   
                        }      

                        self.io.put(url, flow)
