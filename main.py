import asyncio
from alpaca_trade_api.stream import Stream
import scratchapi

# Alpaca API keys
ALPACA_API_KEY = 'PKKU32QA474CHRCDPKXE3ZYBDC'
ALPACA_SECRET_KEY = 'AJzqgFtAm7MFm5jeGFqV4o61Sk4RwFbpgH8YEBZfayb'

# Scratch Credentials
SCRATCH_USERNAME = 'EncryptedCat'
SCRATCH_PASSWORD = 'Encrypted123'
SCRATCH_PROJECT_ID = 1232213894

SCRATCH_CLOUD_VAR_NAME = 'StockPrice'
STOCK_VARS = {
    'AAPL': 'ApplePrice',
    'NVDA': 'NvidiaPrice',
    'TSLA': 'TeslaPrice'
}

# Initialize Scratch session
scratch_session = scratchapi.ScratchUserSession(SCRATCH_USERNAME, SCRATCH_PASSWORD)

async def handle_quote(q, stock):
    price = q.price if hasattr(q, 'price') else None
    if price is not None:
        print(f"{stock} price: {price}")
        var_name = STOCK_VARS[stock]
        # Set cloud variable for this stock
        scratch_session.cloud.set_var(var_name, price, SCRATCH_PROJECT_ID)

async def main():
    stream = Stream(ALPACA_API_KEY, ALPACA_SECRET_KEY, data_feed='iex')  # or 'sip' for paid plans
    # Subscribe to quotes for all three stocks
    for stock in STOCK_VARS.keys():
        stream.subscribe_quotes(lambda q, stock=stock: asyncio.create_task(handle_quote(q, stock)), stock)
    await stream.run()

if __name__ == "__main__":
    asyncio.run(main())

# Run
asyncio.run(main())
