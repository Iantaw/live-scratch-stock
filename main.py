import os
import asyncio
from alpaca_trade_api.stream import Stream
import scratchapi

# Load credentials and project ID from environment variables
SCRATCH_USERNAME = os.getenv('SCRATCH_USERNAME')
SCRATCH_PASSWORD = os.getenv('SCRATCH_PASSWORD')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
SCRATCH_PROJECT_ID = int(os.getenv('SCRATCH_PROJECT_ID'))

# Map stocks to Scratch cloud variable names
STOCK_VARS = {
    'AAPL': 'ApplePrice',
    'NVDA': 'NvidiaPrice',
    'TSLA': 'TeslaPrice'
}

# Initialize Scratch session
scratch_session = scratchapi.ScratchUserSession(SCRATCH_USERNAME, SCRATCH_PASSWORD)

# Async coroutine function as handler for Alpaca quotes
async def handle_quote(q, stock):
    price = getattr(q, 'price', None)
    if price is not None:
        print(f"{stock} price: {price}")
        var_name = STOCK_VARS[stock]
        # Update cloud variable in Scratch project
        scratch_session.cloud.set_var(var_name, price, SCRATCH_PROJECT_ID)

async def main():
    stream = Stream(ALPACA_API_KEY, ALPACA_SECRET_KEY, data_feed='iex')  # or 'sip' if you have paid plan
    # Subscribe asynchronously, scheduling handler with create_task
    for stock in STOCK_VARS:
        stream.subscribe_quotes(lambda q, stock=stock: asyncio.create_task(handle_quote(q, stock)), stock)
    await stream.run()

if __name__ == '__main__':
    asyncio.run(main())
