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
	
	edges = get_topology(ip, port, user, passwd)
	install_flows(edges, ip, port, user, passwd)

# Pull topology
def get_topology(ip, port, user, passwd):
	topology_url = "http://" + str(ip) + ":" + str(port) + \
				"/controller/nb/v2/topology/default/"
	http_context = httplib2.Http(".Cache")
	http_context.add_credentials(user, passwd)
	resp,content = http_context.request(topology_url, "GET")
	edges = json.loads(content)
	return edges

# Install base rules 
def install_flows(edges, ip, port, user, passwd):
	http_context = httplib2.Http(".Cache")
	http_context.add_credentials(user, passwd)
	
	for edge in edges["edgeProperties"]:
		tail = edge["edge"]["tailNodeConnector"]
		head = edge["edge"]["headNodeConnector"]
		url = "http://" + str(ip) + ":" + str(port) + \
				"/controller/nb/v2/flowprogrammer/default/node/OF/" + \
				str(tail["node"]["id"]) + "/staticFlow/normal_" + tail["id"]
		flow = { 
			"installInHw":"true",
			"name":"normal_" + tail["id"],
			"node": {
					"id":str(tail["node"]["id"]),
					"type":"OF"
                    }, 
			"ingressPort":str(tail["id"]), 
 			"etherType":"0x0800",
			"priority":"100",
       		"actions":["HW_PATH"]
		}
		resp, content = http_context.request(url, "PUT", body=str(json.dumps(flow)),\
                           		  headers={"Content-Type":"application/json"})
	
		url = "http://" + str(ip) + ":" + str(port) +\
				"/controller/nb/v2/flowprogrammer/deault/node/OF/" +\
				str(head["node"]["id"]) + "/staticFlow/normal_" + head["id"]
		flow = {
			"installInHw":"true",
			"name":"normal_" + head["id"],
			"node": {
					"id":str(head["node"]["id"]),
					"type":"OF"
					},
			"ingressPort":str(head["id"]),
			"etherType":"0x0800",
			"priority":"100",
			"actions":["HW_PATH"]
		}
		resp, content = http_context.request(url, "PUT", body=str(json.dumps(flow)),\
											headers={"Content-Type":"application/json"})
if __name__ == "__main__":
	main()
