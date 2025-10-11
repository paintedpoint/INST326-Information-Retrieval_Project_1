
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import PullData, display_market_data

dataPuller = PullData()
print("=" * 60)
print("Testing Crypto Data Manager")
print("=" * 60)

# Get market data and display with color-coded arrows
print("\nGetting top 10 cryptocurrencies by market cap...")
market_data = dataPuller.get_market_data()
display_market_data(market_data)

# Get crypto details
print("\nGetting Bitcoin details...")
btc_details = dataPuller.get_crypto_details('bitcoin')
print(f"Name: {btc_details['name']}")
print(f"Price: ${btc_details['current_price']:,.2f}")
print(f"Description: {btc_details['description'][:200]}...")

# Get historical data
print("\nGetting 7-day historical data for Bitcoin...")
eth_history = dataPuller.get_historical_data('bitcoin', days=7)
print(eth_history.tail())