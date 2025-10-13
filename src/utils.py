import pandas as pd

def display_market_data(df: pd.DataFrame, limit: int = 10):
    """
    Displays formatted crypto data with color-coded arrows for price movement.
    Work by Linwood
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

def summarize_market_performance(df: pd.DataFrame) -> None:
    """
    Display the top gainer and top loser from the cryptocurrency dataset.
    Work by Linwood
    Args:
        df (pd.DataFrame): Market data from PullData.get_market_data().
            Must include a 'change_24h' column.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input 'df' must be a pandas DataFrame.")
    if df.empty:
        print("⚠️  No data available for summary.")
        return
    if "change_24h" not in df.columns:
        raise ValueError("DataFrame must include a 'change_24h' column.")

    try:
        top_gainer = df.loc[df["change_24h"].idxmax()]
        top_loser = df.loc[df["change_24h"].idxmin()]

        print("\n📈 Market Performance Summary")
        print("-" * 40)
        print(f"🔼 Top Gainer: {top_gainer['name']} ({top_gainer['symbol'].upper()}) +{top_gainer['change_24h']:.2f}%")
        print(f"🔻 Top Loser: {top_loser['name']} ({top_loser['symbol'].upper()}) {top_loser['change_24h']:.2f}%")
        print("-" * 40)
    except Exception:
        print("⚠️  Could not compute summary statistics.")

def user_interaction(df: pd.DataFrame) -> None:
    """
    Provide an interactive console menu for users to view cryptocurrency data.
    Work by Linwood
    Args:
        df (pd.DataFrame): Market data from PullData.get_market_data().
    """
    if df.empty:
        print("⚠️  No market data available for interaction.")
        return

    while True:
        print("\n=== CRYPTO TRACKER MENU ===")
        print("1. View top 10 cryptocurrencies")
        print("2. View top gainer/loser summary")
        print("3. Exit")
        choice = input("Select an option (1–3): ").strip()

        if choice == "1":
            display_market_data(df, limit=10)
        elif choice == "2":
            summarize_market_performance(df)
        elif choice == "3":
            print("👋 Exiting crypto tracker. Goodbye!")
            break
        else:
            print("❌ Invalid selection. Please enter 1, 2, or 3.")

