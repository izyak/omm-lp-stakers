import csv

sanu = []
with open('liquidity-provider.csv') as file:
	csv_reader = csv.reader(file, delimiter=',')
	for row in csv_reader:
		sanu.append(row[0])
# 1st is title, last is total
sanu_data = (sanu[1:-1])


newton = []
with open('stakedDetail.csv') as file:
	csv_reader = csv.reader(file, delimiter=',')
	for row in csv_reader:
		newton.append(row[0])
# 1st is title, last is total
newton_data = (newton[1:])

print([item for item in sanu_data if item not in newton_data])

