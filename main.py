import os
import asyncio
from alpaca_trade_api.stream import Stream
import scratchapi

# Read credentials and project ID from env variables (set in GitHub Secrets)
SCRATCH_USERNAME = os.getenv('SCRATCH_USERNAME')
SCRATCH_PASSWORD = os.getenv('SCRATCH_PASSWORD')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
SCRATCH_PROJECT_ID = int(os.getenv('SCRATCH_PROJECT_ID'))

# Stock to cloud variable mapping
STOCK_VARS = {
    'AAPL': 'ApplePrice',
    'NVDA': 'NvidiaPrice',
    'TSLA': 'TeslaPrice'
}

# Initialize Scratch session
scratch_session = scratchapi.ScratchUserSession(SCRATCH_USERNAME, SCRATCH_PASSWORD)

async def handle_quote(q, stock):
    price = getattr(q, 'price', None)
    if price is not None:
        print(f"{stock} price: {price}")
        var_name = STOCK_VARS[stock]
        # Update cloud variable
        scratch_session.cloud.set_var(var_name, price, SCRATCH_PROJECT_ID)

async def main():
    stream = Stream(ALPACA_API_KEY, ALPACA_SECRET_KEY, data_feed='iex')  # use 'iex' or 'sip' if paid
    for stock in STOCK_VARS.keys():
        stream.subscribe_quotes(lambda q, stock=stock: asyncio.create_task(handle_quote(q, stock)), stock)
    await stream.run()

if __name__ == '__main__':
    asyncio.run(main())
