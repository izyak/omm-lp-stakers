import concurrent.futures
import json
import requests
import sys
import time
from pprint import pprint
from checkscore.repeater import retry

DEX = "cxa0af3165c08318e988cb30993b3048335b94af6c"
STAKED_LP = "cx015c7f8884d43519aa2bcf634140bd7328730cb6"
LIST_API = "https://main.tracker.solidwallet.io/v3/contract/txList"
TX_DETAIL_API = "https://main.tracker.solidwallet.io/v3/transaction/txDetail"
txnHashes = []
wallets = []

print("Fetching transaction hashes")
@retry(Exception, tries=20, delay=1, back_off=2)
def get_txn_hashes(page):
	payload = {'page': page, 'count': 100, "addr": DEX}
	req = requests.get(LIST_API, params=payload)
	data = json.loads(req.text).get("data")
	for d in data:
	  txnHashes.append(d.get('txHash'))

start_time = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
	executor.map(get_txn_hashes, [i for i in range(0,int(sys.argv[1]))])
end_time = time.perf_counter()
print(f"Took total of {end_time-start_time} seconds to fetch data")
print(f"Total of: {len(txnHashes)} transactions")
print(f"Querying each transaction")

@retry(Exception, tries=20, delay=1, back_off=2)
def get_tx_details(txHash):
	req = requests.get(f"https://main.tracker.solidwallet.io/v3/transaction/txDetail?txHash={txHash}")
	details = json.loads(req.text).get("data")
	if details.get("status") == "Success":
		dataString = details.get("dataString")
		if dataString:
			dataString = json.loads(dataString)
			if dataString.get("method") == "transfer" and dataString.get("params").get("_to") == STAKED_LP:
				wallets.append(details.get("fromAddr"))

start_time = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
	future = executor.map(get_tx_details, txnHashes)

end_time = time.perf_counter()
print(f"Took total of {end_time-start_time} seconds to query all transactions")

with open("wallets.json",'w') as outfile:
  json.dump(list(set(wallets)), outfile)
