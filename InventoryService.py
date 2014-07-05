import httplib2
import json

class InventoryService:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.hosts = []
        self.indexDict = {}

    def setIOService(self, io):
        self.io = io
   
    def initAll(self):
        self.initHosts()
        self.initPRNodes()
        self.initNodes()
        self.initEdges()

    def initPRNodes(self):
        for edge in self.edges:
            if edge["edge"]["tailNodeConnector"]["node"]["type"] == "PR":
                node = {
                    "properties":{
                        "description":edge["edge"]["tailNodeConnector"]["node"]["id"]
                    },
                    "node":{
                        "id":edge["edge"]["tailNodeConnector"]["node"]["id"]
                    }
                }
                if node not in self.nodes:
                    self.nodes.append(node)
 
    def initNodes(self):
        for node in self.nodes:
            node["neighbours"] = {}
            self.indexDict[node["node"]["id"]] = self.nodes.index(node)
            
    def initHosts(self):
        for host in self.hosts:
            self.nodes.append(host)
            self.indexDict[host["dataLayerAddress"]] = self.nodes.index(host)
            self.edges.append({
                "source":self.indexDict[host["dataLayerAddress"]],
                "target":self.indexDict[host["nodeId"]]
            })

    def initEdges(self):
        for edge in self.edges:
            if edge["edge"]:
                edge["source"] = self.indexDict[edge["edge"]["headNodeConnector"]["node"]["id"]]
                edge["target"] = self.indexDict[edge["edge"]["tailNodeConnector"]["node"]["id"]]
                source = edge["source"]
                target = edge["target"]
                self.nodes[source]["neighbours"][target] = edge["edge"]["headNodeConnector"]["id"]
                self.nodes[target]["neighbours"][source] = edge["edge"]["tailNodeConnector"]["id"]
            else:
                self.nodes[target]["neighbours"][source] = self.nodes[source]["nodeConnectorId"]
 
    def getNodesFromController(self):
        url = "/controller/nb/v2/switchmanager/default/nodes"
        content = self.io.get(url)
        self.nodes = json.loads(content)["nodeProperties"]
    
    def getEdgesFromController(self):
        url = "/controller/nb/v2/topology/default"
        content = self.io.get(url)
        self.edges = json.loads(content)["edgeProperties"]

    def getHostsFromController(self):
        url = "/controller/nb/v2/hosttracker/default/hosts/active"
        content = self.io.get(url)
        self.hosts = json.loads(content)["hostConfig"]

    def getNodes(self):
        return self.nodes
    
    def getEdges(self):
        return self.edges
   
    def getHosts(self):
        return self.hosts
