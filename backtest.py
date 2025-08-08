import csv
import sys
from typing import List

from strategy import generate_signals


def read_close_prices(path: str) -> List[float]:
    """Read closing prices from a CSV file.

    The CSV must contain a column named "close".
    """
    prices = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if "close" not in reader.fieldnames:
            raise ValueError("CSV file must contain a 'close' column")
        for row in reader:
            prices.append(float(row["close"]))
    return prices


def compute_profit(prices: List[float], signals: List[str]) -> float:
    """Compute profit of a simple long-only strategy."""
    position = None
    entry = 0.0
    profit = 0.0
    for price, signal in zip(prices, signals):
        if position is None and signal == "BUY":
            position = "long"
            entry = price
        elif position == "long" and signal == "SELL":
            profit += price - entry
            position = None
    if position == "long":
        profit += prices[-1] - entry
    return profit


def run_backtest(prices: List[float]):
    signals = generate_signals(prices)
    profit = compute_profit(prices, signals)
    return profit, signals


def main():
    if len(sys.argv) > 1:
        prices = read_close_prices(sys.argv[1])
    else:
        prices = [100 + i * 0.1 for i in range(100)]
    profit, signals = run_backtest(prices)
    print(f"Final profit: {profit:.2f}")
    for price, signal in zip(prices, signals):
        print(f"Price: {price:.2f}, Signal: {signal}")


if __name__ == "__main__":
    main()
