import json
import csv

with open('walletsList.json') as f:
	data = json.load(f)

with open('stakedDetail.csv', 'w') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)