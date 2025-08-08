# This module implements a basic trading strategy combining
# dual moving averages, MACD, and Bollinger Bands.
# This code is for illustrative purposes only and is not financial advice.

from typing import List, Tuple


def simple_moving_average(prices: List[float], period: int) -> List[float]:
    if period <= 0:
        raise ValueError("period must be positive")
    sma = []
    for i in range(len(prices)):
        if i + 1 < period:
            sma.append(None)
        else:
            window = prices[i + 1 - period : i + 1]
            sma.append(sum(window) / period)
    return sma


def exponential_moving_average(prices: List[float], period: int) -> List[float]:
    if period <= 0:
        raise ValueError("period must be positive")
    ema = []
    k = 2 / (period + 1)
    for i, price in enumerate(prices):
        if i == 0:
            ema.append(price)
        else:
            ema.append(price * k + ema[i - 1] * (1 - k))
    return ema


def macd(prices: List[float], short_period: int = 12, long_period: int = 26, signal_period: int = 9) -> Tuple[List[float], List[float]]:
    ema_short = exponential_moving_average(prices, short_period)
    ema_long = exponential_moving_average(prices, long_period)
    macd_line = [s - l for s, l in zip(ema_short, ema_long)]
    signal_line = exponential_moving_average(macd_line, signal_period)
    return macd_line, signal_line


def bollinger_bands(prices: List[float], period: int = 20, num_std: float = 2) -> Tuple[List[float], List[float], List[float]]:
    if period <= 0:
        raise ValueError("period must be positive")
    sma = simple_moving_average(prices, period)
    upper, lower = [], []
    for i in range(len(prices)):
        if i + 1 < period:
            upper.append(None)
            lower.append(None)
        else:
            window = prices[i + 1 - period : i + 1]
            mean = sma[i]
            variance = sum((p - mean) ** 2 for p in window) / period
            std = variance ** 0.5
            upper.append(mean + num_std * std)
            lower.append(mean - num_std * std)
    return upper, sma, lower


def generate_signals(prices: List[float]) -> List[str]:
    if not prices:
        return []

    fast_period = 10
    slow_period = 30

    fast_ma = simple_moving_average(prices, fast_period)
    slow_ma = simple_moving_average(prices, slow_period)
    macd_line, signal_line = macd(prices)
    upper_band, mid_band, lower_band = bollinger_bands(prices)

    signals = []
    for i in range(len(prices)):
        if None in (fast_ma[i], slow_ma[i], macd_line[i], signal_line[i], upper_band[i], lower_band[i]):
            signals.append("HOLD")
            continue

        buy_condition = (
            fast_ma[i] > slow_ma[i]
            and macd_line[i] > signal_line[i]
            and prices[i] > upper_band[i]
        )
        sell_condition = (
            fast_ma[i] < slow_ma[i]
            and macd_line[i] < signal_line[i]
            and prices[i] < lower_band[i]
        )

        if buy_condition:
            signals.append("BUY")
        elif sell_condition:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals


if __name__ == "__main__":
    # Example usage with synthetic price data
    example_prices = [100 + i * 0.1 for i in range(100)]
    signals = generate_signals(example_prices)
    for price, signal in zip(example_prices, signals):
        print(f"Price: {price:.2f}, Signal: {signal}")
