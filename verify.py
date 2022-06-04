import json
import requests
from pprint import pprint
from checkscore.repeater import retry
import concurrent.futures

STAKED_LP = "cx015c7f8884d43519aa2bcf634140bd7328730cb6"
# some random addresses to check
ADDRS = ['hx6417a059e35a14f94da09d21448621333def7668', 'hxf6ddf06ffcf1f7ff7c7a3baa7faad3b659cd5a78']

for addr in ADDRS:
	hashes=[]
	def get_request(page):
		req = requests.get(f"https://main.tracker.solidwallet.io/v3/address/txList?page={page}&count=100&address={addr}")
		details = json.loads(req.text).get("data")
		for detail in details:
			hashes.append(detail.get('txHash'))
		if len(details) == 100:
			get_request(page+1)

	get_request(1)

	@retry(Exception, tries=20, delay=1, back_off=2)
	def get_tx_details(txHash):
		req = requests.get(f"https://main.tracker.solidwallet.io/v3/transaction/txDetail?txHash={txHash}")
		details = json.loads(req.text).get("data")
		if details.get("status") == "Success":
			dataString = details.get("dataString")
			if dataString:
				dataString = json.loads(dataString)
				if dataString.get("method") == "transfer" and dataString.get("params").get("_to") == STAKED_LP:
					print(f"LP Staking transaction done by: {addr} :> {txHash}")

	with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
		future = executor.map(get_tx_details, hashes)