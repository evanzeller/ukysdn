from flask import Flask
import InventoryService
import IOService
import PathService

if __name__ == "__main__":
    inv = InventoryService.InventoryService()
    io = IOService.IOService()
    io.setController("172.16.6.12", "8080", "admin", "cc-nie")
    inv.setIOService(io)
    inv.getNodesFromController()       
    inv.getEdgesFromController()
    inv.getHostsFromController()
    inv.initAll()
    ps = PathService.PathService()
    ps.setInventoryService(inv)
    ps.setIOService(io)
    path = ps.dijkstra(4,6)   
    ps.pushPath(path, "test")

    
