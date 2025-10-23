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

async def main():
    stream = Stream(ALPACA_API_KEY, ALPACA_SECRET_KEY, data_feed='iex')
    for stock in STOCK_VARS.keys():
        async def handler(q, stock=stock):
            price = getattr(q, 'price', None)
            if price is not None:
                print(f"{stock} price: {price}")
                var_name = STOCK_VARS[stock]
                scratch_session.cloud.set_var(var_name, price, SCRATCH_PROJECT_ID)
        stream.subscribe_quotes(handler, stock)
    await stream.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "asyncio.run() cannot be called from a running event loop" in str(e):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise
