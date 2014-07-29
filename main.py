from flask import Flask, request, jsonify
import InventoryService
import IOService
import PathService

app = Flask(__name__)

@app.route("/api/flows/<name>", methods=["POST"])
def shortest_path(name):
    req = request.get_json(force=True)
    print req
    src = inv.getNodeIndexByIp(req["srcIp"])
    dst = inv.getNodeIndexByIp(req["dstIp"])
    return jsonify(ps.dijkstra(src, dst))

if __name__ == "__main__":
    inv = InventoryService.InventoryService()
    io = IOService.IOService()
    ps = PathService.PathService()
    io.setController("172.16.6.12", "8080", "admin", "cc-nie")
    inv.setIOService(io)
    inv.getNodesFromController()       
    inv.getEdgesFromController()
    inv.getHostsFromController()
    inv.initAll()
    ps.setInventoryService(inv)
    ps.setIOService(io)
    app.debug = True
    app.run()

    
