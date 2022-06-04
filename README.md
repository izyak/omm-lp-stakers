# LP STAKERS LIST FOR OMM

## How to run the script
```sh
./run.sh
```

This data was calculated at 4:00 PM on 4th of June. (NST)

```json
{
    "6": "1112392210000000000",
    "7": "1942324300000000000000000",
    "8": "1180862870000000000000013"
}
```


## Data Files:

`wallets.json`: List of all addresses that have once provided liquidity to OMM.

`lpStakersDetail.json`: List of all these addresses, along with the number of lpTokens for each pair on OMM.

`lpStakersDetail.csv`: CSV file of lpStakersDetail.json, to view on sheets.

---
## Script Files:
`liquidityProviders.py`: Fetch address list of all the lp providers.

`getPoolBalanceOfAddrs.py`: Get their current staked balance for 3 pools in OMM.

`checkTotalLpStaked.py`: Verify if sum of user's staked balance = total staked balance for each pool.

`jsontocsv.py`: Convert JSON to CSV.

`verify.py`: Check random addresses's transaction history to verify they staked lp tokens at a point.

---
