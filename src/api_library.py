import requests
import pandas as pd
from typing import Dict, List
import time

class PullData:
    """
    Class for fetching and processing data from CoinGecko API
    Work by William
    """

    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3"
        self.last_request_time = 0
        self.rate_limit_delay = 3.0

    def _rate_limit(self):
        """Ensure we don't exceed API rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Make a rate-limited request to the API
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response as dictionary
        """
        self._rate_limit()
        url = f"{self.url}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        
    def get_market_data(self, page: int = 1) -> pd.DataFrame:
        """
        Get current market data for multiple cryptocurrencies
        
        Args:
            page: Page number
            
        Returns:
            DataFrame with market data
        """
        params = {
            "vs_currency": 'usd',
            "order": "market_cap_desc",
            "per_page": 100,
            "page": page,
            "sparkline": False,
            "price_change_percentage": "24h,7d"
        }
        
        data = self._make_request("coins/markets", params)

        if not data:
            return pd.DataFrame()
        
        # Convert to DataFrame and select relevant columns
        df = pd.DataFrame(data)
        df = df[[
            'id', 'symbol', 'name', 'current_price', 
            'market_cap', 'market_cap_rank', 'total_volume',
            'price_change_percentage_24h', 'price_change_percentage_7d_in_currency'
        ]]
        
        # Rename columns
        df = df.rename(columns={
            'price_change_percentage_24h': 'change_24h',
            'price_change_percentage_7d_in_currency': 'change_7d'
        })
        
        return df
    
    def get_crypto_details(self, crypto_id: str) -> Dict:
        """
        Get detailed information about a specific cryptocurrency
        
        Args:
            crypto_id: CoinGecko ID (e.g., 'bitcoin', 'ethereum')
            
        Returns:
            Dictionary with crypto details including description
        """
        data = self._make_request(f"coins/{crypto_id}")
        
        if not data:
            return {}
        
        # Extract only relevant information
        details = {
            'id'                : data.get('id'),
            'symbol'            : data.get('symbol', '').upper(),
            'name'              : data.get('name'),
            'description'       : data.get('description', {}).get('en', 'No description available'),
            'current_price'     : data.get('market_data', {}).get('current_price', {}).get('usd'),
            'market_cap'        : data.get('market_data', {}).get('market_cap', {}).get('usd'),
            'total_volume'      : data.get('market_data', {}).get('total_volume', {}).get('usd'),
            'price_change_24h'  : data.get('market_data', {}).get('price_change_percentage_24h'),
            'all_time_high'     : data.get('market_data', {}).get('ath', {}).get('usd'),
            'all_time_low'      : data.get('market_data', {}).get('atl', {}).get('usd'),
            'homepage'          : data.get('links', {}).get('homepage', [''])[0]
        }
        
        return details
    
    def get_historical_data(self, crypto_id: str, days: int = 30) -> pd.DataFrame:
        """
        Get historical price data for a cryptocurrency
        
        Args:
            crypto_id: CoinGecko ID (e.g., 'bitcoin', 'ethereum')
            days: Number of days of historical data (max 365)
            
        Returns:
            DataFrame with timestamp and price columns
        """
        params = {
            "vs_currency": 'usd',
            "days": days
        }
        
        data = self._make_request(f"coins/{crypto_id}/market_chart", params)
        
        if not data or 'prices' not in data:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['date'] = df['timestamp'].dt.date
        
        return df
    
    def get_current_price(self, crypto_ids: List[str], vs_currency: str = "usd") -> Dict:
        """
        Get current prices for multiple cryptocurrencies
        
        Args:
            crypto_ids: List of CoinGecko IDs
            vs_currency: Currency to compare against
            
        Returns:
            Dictionary mapping crypto_id to price
        """
        params = {
            "ids": ",".join(crypto_ids),
            "vs_currencies": vs_currency
        }
        
        data = self._make_request("simple/price", params)
        if not data:
            return {}
        
        # Flatten the nested structure
        prices = {crypto_id: info.get(vs_currency, 0) 
                 for crypto_id, info in data.items()}
        
        return prices
    
