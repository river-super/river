# river

This repository contains a simple example of a trading strategy implemented in Python.
It combines dual moving averages, the MACD indicator, and Bollinger Bands to
produce buy and sell signals. The code is for educational purposes and does not
constitute financial advice.

## Running the example

The strategy is implemented in `strategy.py`. To see it in action with synthetic
data, run:

```bash
python strategy.py
```

The script will output generated signals for the example price series.

## Backtesting with your own data

You can run a simple backtest using `backtest.py`. Provide a CSV file with a
`close` column (for example exported from Binance) and the script will generate
signals and report the overall profit of a naive long-only strategy:

```bash
python backtest.py path/to/binance_data.csv
```

If no file is supplied, the script falls back to the same synthetic data used in
`strategy.py`.
