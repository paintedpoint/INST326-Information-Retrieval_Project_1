from will import PullData
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List
import time


# ===========================================
# CLASS 1: PullData  (From your teammate)
# ===========================================
class PullData:
    """
    Class for fetching and processing data from CoinGecko API
    """

    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3"
        self.last_request_time = 0
        self.rate_limit_delay = 1.5

    def _rate_limit(self):
        """Ensure we don't exceed API rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a rate-limited request to the API with retries"""
        url = f"{self.url}/{endpoint}"
        retries = 3
        for attempt in range(retries):
            self._rate_limit()
            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 429:
                    print("Rate limit reached, waiting 5 seconds...")
                    time.sleep(5)
                    continue
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"API request failed (attempt {attempt+1}): {e}")
                time.sleep(2)
        print(" Failed after multiple retries.")
        return None

        
    def get_current_price(self, crypto_ids: List[str], vs_currency: str = "usd") -> Dict:
        """Get current prices for multiple cryptocurrencies"""
        params = {"ids": ",".join(crypto_ids), "vs_currencies": vs_currency}
        data = self._make_request("simple/price", params)
        if not data:
            return {}
        return {crypto_id: info.get(vs_currency, 0) for crypto_id, info in data.items()}


# ===========================================
# CLASS 2: CryptoPortfolio  (Your new code)
# ===========================================
class CryptoPortfolio:
    """
    Class to manage cryptocurrency purchases and sales
    """

    def __init__(self, data_puller: PullData):
        self.data_puller = data_puller
        self.holdings = {}  # {crypto_id: {'amount': float, 'avg_buy_price': float}}
        self.transactions = []  # list of transaction dictionaries

    def buy(self, crypto_id: str, amount: float):
        """Buy a specified amount of a cryptocurrency"""
        price_data = self.data_puller.get_current_price([crypto_id])
        if not price_data or crypto_id not in price_data:
            print("Error: Could not fetch price for", crypto_id)
            return
        
        current_price = price_data[crypto_id]
        cost = amount * current_price

        # Update holdings
        if crypto_id in self.holdings:
            prev = self.holdings[crypto_id]
            total_value = prev['amount'] * prev['avg_buy_price'] + cost
            total_amount = prev['amount'] + amount
            prev['amount'] = total_amount
            prev['avg_buy_price'] = total_value / total_amount
        else:
            self.holdings[crypto_id] = {'amount': amount, 'avg_buy_price': current_price}

        # Record transaction
        self.transactions.append({
            'type': 'BUY',
            'crypto': crypto_id,
            'amount': amount,
            'price': current_price,
            'time': datetime.now()
        })
        print(f"Bought {amount} {crypto_id} at ${current_price:.2f} each (${cost:.2f} total)")

    def sell(self, crypto_id: str, amount: float):
        """Sell a specified amount of a cryptocurrency"""
        if crypto_id not in self.holdings or self.holdings[crypto_id]['amount'] < amount:
            print("Error: Not enough holdings to sell.")
            return
        
        price_data = self.data_puller.get_current_price([crypto_id])
        if not price_data or crypto_id not in price_data:
            print("Error: Could not fetch price for", crypto_id)
            return
        
        current_price = price_data[crypto_id]
        proceeds = amount * current_price
        cost_basis = amount * self.holdings[crypto_id]['avg_buy_price']
        profit = proceeds - cost_basis

        self.holdings[crypto_id]['amount'] -= amount
        if self.holdings[crypto_id]['amount'] == 0:
            del self.holdings[crypto_id]

        self.transactions.append({
            'type': 'SELL',
            'crypto': crypto_id,
            'amount': amount,
            'price': current_price,
            'profit': profit,
            'time': datetime.now()
        })
        print(f" Sold {amount} {crypto_id} at ${current_price:.2f} each "
              f"(${proceeds:.2f} total, Profit: ${profit:.2f})")

    def portfolio_value(self):
        """Return the total value of current holdings based on live prices"""
        if not self.holdings:
            print("No holdings in portfolio.")
            return 0.0

        ids = list(self.holdings.keys())
        prices = self.data_puller.get_current_price(ids)
        total_value = 0

        print("\n Current Portfolio Value:")
        for crypto_id in ids:
            amount = self.holdings[crypto_id]['amount']
            price = prices.get(crypto_id, 0)
            value = amount * price
            total_value += value
            print(f" - {crypto_id:<10} {amount:.4f} @ ${price:.2f} = ${value:,.2f}")

        print(f" Total Portfolio Value: ${total_value:,.2f}")
        return total_value

    def show_transactions(self):
        """Display transaction history"""
        if not self.transactions:
            print("No transactions yet.")
            return
        
        print("\n Transaction History:")
        for t in self.transactions:
            if t['type'] == 'BUY':
                print(f"{t['time']} | BUY  {t['amount']} {t['crypto']} @ ${t['price']:.2f}")
            else:
                print(f"{t['time']} | SELL {t['amount']} {t['crypto']} @ ${t['price']:.2f} "
                      f"(Profit: ${t['profit']:.2f})")


# ===========================================
# MAIN TEST DRIVER
# ===========================================
if __name__ == "__main__":
    print("=" * 60)
    print(" CRYPTO PORTFOLIO MANAGER ")
    print("=" * 60)

    data_puller = PullData()
    portfolio = CryptoPortfolio(data_puller)
    prices = data_puller.get_current_price(["bitcoin", "ethereum"])

    # Example buys
    portfolio.buy("bitcoin", 0.001)
    portfolio.buy("ethereum", 0.02)

    # Example sell
    time.sleep(2)
    portfolio.sell("bitcoin", 0.0005)

    # Portfolio summary
    portfolio.portfolio_value()
    portfolio.show_transactions()
