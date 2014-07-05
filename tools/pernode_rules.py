import sys
import httplib2
import json
import getopt

def main():
	opts, args = getopt.getopt(sys.argv[1:], [], ['ip=', 'port=', 'user=', 'passwd='])
	for o, a in opts:
		if o == '--ip':
			ip = a
		if o == '--port':
			port = a
		if o == '--user':
			user = a
		if o == '--passwd':
			passwd = a
	
	nodes = get_nodes(ip, port, user, passwd)
	install_flows(nodes, ip, port, user, passwd)

# Pull nodes from switchmanager API
def get_nodes(ip, port, user, passwd):
	nodes_url = "http://" + str(ip) + ":" + str(port) + \
				"/controller/nb/v2/switchmanager/default/nodes/"
	http_context = httplib2.Http(".Cache")
	http_context.add_credentials(user, passwd)
	resp,content = http_context.request(nodes_url, "GET")
	nodes = json.loads(content)
	return nodes

# Install lldp, arp, dhcp flows for each node in nodes
def install_flows(nodes, ip, port, user, passwd):
	http_context = httplib2.Http(".Cache")
	http_context.add_credentials(user, passwd)
	
	for node in nodes["nodeProperties"]:
		url = 'http://' + str(ip) + ":" + str(port) + \
				"/controller/nb/v2/flowprogrammer/default/node/OF/" + \
				str(node["node"]["id"]) + "/staticFlow/lldp"
		flow = { 
            "installInHw":"true",
            "name":"lldp",
            "node": {
                    "id":str(node["node"]["id"]),
                    "type":"OF"
                    },  
            "etherType":"0x88cc",
			"priority":"100",
            "actions":["CONTROLLER"]
        }
   
		resp, content = http_context.request(url, "PUT", body=str(json.dumps(flow)),\
                           		  headers={'Content-Type':'application/json'})
		
		url = "http://" + str(ip) + ":" + str(port) + \
				"/controller/nb/v2/flowprogrammer/default/node/OF/" +\
				str(node["node"]["id"]) + "/staticFlow/arp"
		flow = {
			"installInHw":"true",
			"name":"arp",
			"node": {
					"id":str(node["node"]["id"]),
					"type":"OF",
					},
			"etherType":"0x0806",
			"priority":"100",
			"actions":["HW_PATH"]
		}
		resp, content = http_context.request(url, "PUT", body=str(json.dumps(flow)),\
										headers={"Content-Type":"application/json"})

		url = "http://" + str(ip) + ":" + str(port) + \
                "/controller/nb/v2/flowprogrammer/default/node/OF/" +\
                str(node["node"]["id"]) + "/staticFlow/dhcp"
		flow = {
            "installInHw":"true",
            "name":"dhcp",
            "node": {
                    "id":str(node["node"]["id"]),
                    "type":"OF",
                    },
            "etherType":"0x0800",
			"priority":"100",
			"protocol":"UDP",
			"tpDst":"67",
            "actions":["HW_PATH"]
        }
		resp, content = http_context.request(url, "PUT", body=str(json.dumps(flow)),\
										headers={"Content-Type":"application/json"})

 
if __name__ == "__main__":
	main()
