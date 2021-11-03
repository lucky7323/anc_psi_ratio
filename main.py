from datetime import datetime
from terra_sdk.client.lcd import LCDClient
from tqdm import tqdm
from loguru import logger
import collections
import requests
import time
import pandas as pd
from fake_useragent import UserAgent


def get_terra_gas_prices():
    try:
        r = requests.get("https://fcd.terra.dev/v1/txs/gas_prices")
        r.raise_for_status()
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.HTTPError as err:
        logger.error(f"Could not fetch get_terra_gas_prices from Terra's FCD. Error message: {err}")


def get_gov_staking_amount(address: str):
    chain_id = 'columbus-5'
    public_node_url = 'https://lcd.terra.dev'
    anc_gov = "terra1f32xyep306hhcxxxf7mlyh0ucggc00rm2s9da5"

    terra = LCDClient(
        chain_id=chain_id,
        url=public_node_url,
        gas_prices=get_terra_gas_prices(),
        gas_adjustment=1.6)

    query_msg = {'staker': {
        'address': address
    }}

    return float(terra.wasm.contract_query(anc_gov, query_msg)['balance']) / 1000000


def main():
    ts_thres = datetime(year=2021, month=10, day=31)
    nexus_addr = "terra1992lljnteewpz0g398geufylawcmmvgh8l8v96"
    base_url = f"https://fcd.terra.dev/v1/txs?account={nexus_addr}&limit=100&offset="
    offset = 0
    is_stop = False
    data_size = 10000
    data = collections.defaultdict(list)
    pbar = tqdm(total=data_size)

    while True:
        if len(data['anc']) > data_size:
            break
        ua = UserAgent()
        headers = {'User-Agent': ua.random,}

        logger.info(f"offset: {offset}")
        response = requests.get(f"{base_url}{offset}", headers=headers)
        time.sleep(0.2)
        if not response or response.status_code != 200:
            break
        response = response.json()
        if 'next' in response:
            offset = response['next']
        else:
            is_stop = True

        for tx in response['txs']:
            if ts_thres > datetime.strptime(tx['timestamp'], '%Y-%m-%dT%H:%M:%SZ'):
                is_stop = True
                break
            value = tx['tx']['value']['msg'][0]['value']
            addr = value['sender']
            airdrop_amount = float(value['execute_msg']['claim']['amount']) / 1000000
            anc_staking_amount = get_gov_staking_amount(addr)
            if anc_staking_amount < 100:
                continue
            data['anc'].append(anc_staking_amount)
            data['psi'].append(airdrop_amount)
            pbar.update(1)
        if is_stop:
            break

    pbar.close()
    df = pd.DataFrame(data)
    df.to_csv("data.csv", index=False)


if __name__ == "__main__":
    logger.remove()
    logger.add("offsets.log")
    main()

