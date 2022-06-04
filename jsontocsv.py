import json
import csv

with open('lpStakersDetail.json') as f:
	data = json.load(f)

with open('lpStakersDetail.csv', 'w') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)