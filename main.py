from flask import Flask
import InventoryService
import IOService
import PathService

if __name__ == "__main__":
    inv = InventoryService.InventoryService()
    io = IOService.IOService()
    io.setController("172.24.240.19", "8080", "admin", "cc-nie")
    inv.setIOService(io)
    inv.getNodesFromController()       
    inv.getEdgesFromController()
    inv.getHostsFromController()
    inv.initAll()
    ps = PathService.PathService()
    ps.setInventoryService(inv)
    ps.dijkstra(0, 3)    
    
