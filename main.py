from flask import Flask, request, jsonify
import InventoryService
import IOService
import PathService

app = Flask(__name__)

@app.route("/rest/paths/<name>", methods=["POST"])
def add_path(name):
    paths = inv.getPaths()
    if name in paths:
        print "Path with that identifier already exists"
        return
    req = request.get_json(force=True)
    print req
    src = inv.getNodeIndexByIp(req["srcIp"])
    dst = inv.getNodeIndexByIp(req["dstIp"])
    # append to store of paths
    # on shutdown we will try to write this to a file
    path = ps.dijkstra(src, dst)
    inv.add_path(name, path)
    ps.pushPath(name, path)
    return jsonify(path)

@app.route("/rest/paths/<name>", methods=["DELETE"])
def remove_path(name):
    req = request.get_json(force=True)
    inv.remove_path(name)
    
if __name__ == "__main__":
    inv = InventoryService.InventoryService()
    io = IOService.IOService()
    ps = PathService.PathService()
    io.setController("172.24.240.19", "8080", "admin", "cc-nie")
    inv.setIOService(io)
    inv.getNodesFromController()       
    inv.getEdgesFromController()
    inv.getHostsFromController()
    inv.initAll()
    ps.setInventoryService(inv)
    ps.setIOService(io)
    app.debug = True
    app.run()

    
