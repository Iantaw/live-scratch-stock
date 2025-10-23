import os
import asyncio
from alpaca_trade_api.stream import Stream
import scratchapi

ALPACA_API_KEY = 'PKKU32QA474CHRCDPKXE3ZYBDC'
ALPACA_SECRET_KEY = 'AJzqgFtAm7MFm5jeGFqV4o61Sk4RwFbpgH8YEBZfayb'

# Scratch Credentials
SCRATCH_USERNAME = 'EncryptedCat'
SCRATCH_PASSWORD = 'Encrypted123'
SCRATCH_PROJECT_ID = 1232213894

STOCK_VARS = {
    'AAPL': 'ApplePrice',
    'NVDA': 'NvidiaPrice',
    'TSLA': 'TeslaPrice'
}

scratch_session = scratchapi.ScratchUserSession(SCRATCH_USERNAME, SCRATCH_PASSWORD)

async def main():
    # Set base_url for paper trading explicitly
    stream = Stream(
        ALPACA_API_KEY,
        ALPACA_SECRET_KEY,
        base_url='https://paper-api.alpaca.markets',
        data_feed='iex'  # Use IEX for paper trading
    )
    for stock in STOCK_VARS.keys():
        async def handler(q, stock=stock):
            price = getattr(q, 'price', None)
            if price is not None:
                print(f"{stock} price: {price}")
                var_name = STOCK_VARS[stock]
                scratch_session.cloud.set_var(var_name, price, SCRATCH_PROJECT_ID)
        stream.subscribe_quotes(handler, stock)
    await stream._run_forever()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
