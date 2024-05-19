def swing_trade_fn(df, low_threshold):
    max_profit = -float('inf')
    start_date = None
    end_date = None
    open_prices = df['Open']
    print(open_prices)
    for i, (date, sell_price) in enumerate(open_prices.items()):
        for date2, buy_price in open_prices.iloc[i + 1:].items():  # Start from i+1
            if max_profit < sell_price - buy_price:
                max_profit = sell_price - buy_price
                start_date = date
                end_date = date2
                print(start_date, end_date)

    if max_profit <= low_threshold:
        return None, None

    if open_prices[end_date] > df['Close'].iloc[-1]:
        end_date = None

    return start_date, end_date
