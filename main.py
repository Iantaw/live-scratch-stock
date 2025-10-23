import os
import asyncio
from alpaca_trade_api.stream import Stream
import scratchapi

SCRATCH_USERNAME = os.getenv('SCRATCH_USERNAME')
SCRATCH_PASSWORD = os.getenv('SCRATCH_PASSWORD')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
SCRATCH_PROJECT_ID = int(os.getenv('SCRATCH_PROJECT_ID'))

STOCK_VARS = {
    'AAPL': 'ApplePrice',
    'NVDA': 'NvidiaPrice',
    'TSLA': 'TeslaPrice'
}

scratch_session = scratchapi.ScratchUserSession(SCRATCH_USERNAME, SCRATCH_PASSWORD)

async def make_handler(stock):
    async def handler(q):
        price = getattr(q, 'price', None)
        if price is not None:
            print(f"{stock} price: {price}")
            var_name = STOCK_VARS[stock]
            scratch_session.cloud.set_var(var_name, price, SCRATCH_PROJECT_ID)
    return handler

async def main():
    stream = Stream(ALPACA_API_KEY, ALPACA_SECRET_KEY, data_feed='iex')
    for stock in STOCK_VARS.keys():
        handler = await make_handler(stock)
        stream.subscribe_quotes(handler, stock)
    await stream.run()

if __name__ == "__main__":
    asyncio.run(main())
