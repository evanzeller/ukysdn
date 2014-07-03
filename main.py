from flask import Flask
import InventoryService
import IOService

if __name__ == "__main__":
    inv = InventoryService.InventoryService()
    io = IOService.IOService()
    io.setController("127.0.0.1", "8080", "admin", "admin")
    inv.setIOService(io)
    inv.getNodesFromController()       
    inv.getEdgesFromController()
    inv.initAll()
    print inv.getEdges() 
