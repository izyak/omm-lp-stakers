# !bin/bash/python

# upto 2000 pages (2000 * 100 total transactions)
python3 ./liquidityProviders.py 2000 
python3 ./getPoolBalanceOfAddrs.py
python3 ./checkTotalLpStaked.py
python3 ./jsontocsv.py