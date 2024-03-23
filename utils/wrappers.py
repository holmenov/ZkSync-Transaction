import asyncio
import sys
from loguru import logger
from web3 import Web3

from settings import MainSettings as SETTINGS
from utils.utils import async_sleep


def check_gas(func):
    async def wrapper(*args, **kwargs):
        w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))
        gas_price_gwei = round(w3.from_wei(w3.eth.gas_price, 'gwei'), 0)

        if gas_price_gwei > SETTINGS.MAX_GAS:
            logger.warning(f'The gas value is higher than the value set in MAX_GAS. Expecting a decrease in the GAS price. Current gas: {gas_price_gwei} gwei.')

            while gas_price_gwei > SETTINGS.MAX_GAS:
                await asyncio.sleep(1)

        await func(*args, **kwargs)

    return wrapper         