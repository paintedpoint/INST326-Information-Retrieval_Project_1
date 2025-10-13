import requests
import pandas as pd 
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta


def calculate_value_portfolio(holdings: Dict[str, float], df: pd.DataFrame) -> float:
    """
    Calculates the total value from a Cypto Portfolio
    Works by Christophera
    Args:
    holdings (dict): Dictionary with crypto symbols as keys and quantities as values
                        Example: {'BTC': 0.5, 'ETH': 2.0}
        df (pd.DataFrame): Market data with 'symbol' and 'current_price' columns
        
    Returns:
        float: Total portfolio value in USD
    
    """
    if not isinstance(holdings, dict):
        raise TypeError("Holding must be a type -> dictionary")
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a dataframe from Pandas")
    if df.empty:
        return 0.0
    if 'symbol' not in df.columns or 'current_price' not in df.columns:
        raise ValueError("DataFrame must contain Symbol and Current_price Column")
    
    total = 0.0
    df_lower = df.copy()
    df_lower['symbol'] = df_lower['symbol'].str.lower()

    for symbol, quantity in holdings.items():
        symbol_lower = symbol.lower()
        crypto_info = df_lower[df_lower['symbol'] == symbol_lower]
        if not crypto_info.empty:
            price = crypto_info.iloc[0]['current_price']
            total += price * quantity
    
    return round(total, 2)

def calculate_returns_portfolio(holdings: Dict[str, float], df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate the 24hrs returns for the Portfolio based on Changes
    Works by Christopher

    Args:
        holdings (dict): Dictionary with crypto symbols as keys and quantities as values
        df (pd.DataFrame): Market data with 'symbol', 'current_price', and 'change_24h' columns
    Returns:
        dict: Dictionary with keys 'total_value', 'total_change_usd', 'total_change_percent'
        
    """
     
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a dataframe from Pandas")
    if df.empty:
        return {'Total Value': 0.0, 'Total Change USD': 0.0, 'Total Change %': 0.0}
    new_cols = ['symbol', 'current_price', 'change_24h']
    if not all(col in df.columns for col in new_cols):
         raise ValueError(f"Dataframe needs to contain colums: {new_cols}")
     
    df_lower = df.copy()
    df_lower['symbol'] = df_lower['symbol'].str.lower()

    curr_value = 0.0
    last_value = 0.0
     
    for symbol, quantity in holdings.items():
         symbol_lower = symbol.lower() 
         crypto_data = df_lower[df_lower['symbol'] == symbol_lower]

         if not crypto_data.empty:
             curr_price = crypto_data.iloc[0]['current_price']
             hrs_change = crypto_data.iloc[0]['change_24h']

             if pd.notna(hrs_change) and pd.notna(curr_price):
                 last_price = curr_price / (1 + hrs_change / 100)
                 curr_value += curr_price * quantity
                 last_value += last_price * quantity
    
    convert_usd = curr_value - last_value
    precent_change = (convert_usd/ last_value * 100) if last_value > 0 else 0.0

    return {
         'Total Value': round(curr_value, 2),
         'Total USD' : round(convert_usd, 2),
         'Total Change %': round(precent_change, 2)
     }


def portfolio_display(holdings: Dict[str, float], df: pd.DataFrame) -> None:
    """
    Display a full summary of portfolio holdings and overall performance.
    Works by Christopher 

    Args:
        holdings (dict): Dictionary with crypto symbols as keys and quantities as values
        df (pd.DataFrame): Market data from PullData.get_market_data()
        
    Examples:
        >>> display_portfolio_summary({'btc': 0.5, 'eth': 10}, market_df)

    """
    if not holdings:
        print("(ERROR) Portfolio is empty :(")
        return
    if df.empty:
        print("(ERROR) No Market Data")
        return

    try:
        total = calculate_value_portfolio(holdings, df)
        returns = calculate_returns_portfolio (holdings, df)

        print("\n PORTFOLIO SUMMARY")
        print ("=" * 50)
        print(f"Total Value: ${total:,.2f}")

        convert_usd = returns['Total USD']
        convert_pct = returns['Total Change %']

        if convert_pct >= 0:
            color = "\033[92m"
            arr = "DOWN"
            sign = "+"
        else:
            color = "\033[91m"
            arr = "UP"
            sign = ""
        print(f"24hrs Change: {color}{arr} {sign}${abs(convert_usd):,.2f} ({sign}{convert_pct:.2f}%)")
        print("=" * 50)
        
    except Exception as e:
        print(f"ERROR with portfolio {str(e)}")



   