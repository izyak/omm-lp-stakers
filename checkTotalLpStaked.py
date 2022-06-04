import json
import requests
from pprint import pprint

with open('lpStakersDetail.json') as f:
	data = json.load(f)

# calculate
data=data[1:]
sicx_sum = 0
iusdc_sum = 0
usds_sum = 0
for row in data:
	iusdc = row[1]
	sicx = row[2]
	usds = row[3]
	iusdc_sum += iusdc
	sicx_sum += sicx
	usds_sum += usds

expected={}
expected[6]=iusdc_sum
expected[7]=sicx_sum
expected[8]=usds_sum

# score data
actual={}
def get_data():
	rpc_dict = {
	    "jsonrpc": "2.0",
	    "method": "icx_call",
	    "id": 1234,
	    "params": {
	        "from": "hxbe258ceb872e08851f1f59694dac2558708ece11", 
	        "to": "cx015c7f8884d43519aa2bcf634140bd7328730cb6",
	        "dataType": "call",
	        "data": {
	            "method": "getBalanceByPool",
	            "params": {}
	        }
	    }
	}
	r = requests.post("https://ctz.solidwallet.io/api/v3", data=json.dumps(rpc_dict))
	pools = json.loads(r.text)['result']
	for pool in pools:
		actual[int(pool['poolID'],0)] = int(pool['totalStakedBalance'],0)
get_data()

pprint(expected)
pprint(actual)
assert expected == actual