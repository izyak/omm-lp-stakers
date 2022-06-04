import json
import requests
from checkscore.repeater import retry
import csv
import concurrent.futures

csvList = [["wallet","iusdc","sicx","usds"]]
count = 0
with open('wallets.json') as f:
	data = json.load(f)

@retry(Exception, tries=20, delay=1, back_off=2)
def get_data(wallet):
	rpc_dict = {
	    "jsonrpc": "2.0",
	    "method": "icx_call",
	    "id": 1234,
	    "params": {
	        "from": "hxbe258ceb872e08851f1f59694dac2558708ece11", 
	        "to": "cx015c7f8884d43519aa2bcf634140bd7328730cb6",
	        "dataType": "call",
	        "data": {
	            "method": "getPoolBalanceByUser",
	            "params": {
	                "_owner": wallet 
	            }
	        }
	    }
	}
	r = requests.post("https://ctz.solidwallet.io/api/v3", data=json.dumps(rpc_dict))
	pools = json.loads(r.text)['result']
	row = [wallet]

	for pool in pools:
		if pool.get('poolID') == "0x6":
			iusdc_bal = int(pool.get('userStakedBalance'),0)
		if pool.get('poolID') == "0x7":
			sicx_bal = int(pool.get('userStakedBalance'),0)
		if pool.get('poolID') == "0x8":
			usds_bal = int(pool.get('userStakedBalance'),0)

	row.append(iusdc_bal)
	row.append(sicx_bal)
	row.append(usds_bal)
	csvList.append(row)

if __name__ == '__main__':
	with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
		executor.map(get_data, data)
	with open("lpStakersDetail.json",'w') as outfile:
  		json.dump(csvList, outfile)