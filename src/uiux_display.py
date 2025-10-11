
import pandas as pd

def display_market_data(df: pd.DataFrame, limit: int = 10):
    """
    Displays formatted crypto data with color-coded arrows for price movement.
    
    Args:
        df (pd.DataFrame): Market data from PullData.get_market_data()
        limit (int): Number of rows to display (default: 10)
    """
    if df.empty:
        print("⚠️  No data available to display.")
        return

    print("\n{:<20} {:<10} {:>12} {:>12}".format("Name", "Symbol", "Price (USD)", "24h Change"))
    print("-" * 60)

    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    for _, row in df.head(limit).iterrows():
        name = row['name']
        symbol = row['symbol'].upper()
        price = row['current_price']
        change = row['change_24h']

        if pd.isna(change):
            color = RESET
            arrow = ""
            formatted_change = "N/A"
        elif change > 0:
            color = GREEN
            arrow = "▲"
            formatted_change = f"{arrow} +{change:.2f}%"
        else:
            color = RED
            arrow = "▼"
            formatted_change = f"{arrow} {change:.2f}%"

        print("{:<20} {:<10} {:>12,.2f} {}{:>12}{}".format(
            name, symbol, price, color, formatted_change, RESET
        ))

    print("-" * 60)