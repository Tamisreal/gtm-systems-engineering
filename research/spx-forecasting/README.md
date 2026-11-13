# SPX probabilistic range study

Not a tested model. No accuracy is claimed.

This sits outside the sales and marketing (GTM) projects on purpose. It is here because the way it fails teaches something to anyone building scores or forecasts on sales data. Using information you would not have had at the time makes a trading tool look accurate. The same mistake makes a churn model or a lead score look accurate.

## What it is

A TradingView indicator (a chart add-on written in TradingView's Pine Script language) that draws a likely high-to-low range for the S&P 500 index for the day. It works in three steps:

1. Take each past day's range (high minus low) and divide it by ATR (Average True Range, a standard measure of how much the index usually moves in a day).
2. Find where those adjusted ranges usually fall, for example the level that 80% of past days stayed under (a percentile).
3. Multiply those levels by today's ATR to draw bands on the chart, each with a stated chance of holding the day's range.

```
normalized_range(d) = (high(d) - low(d)) / ATR(d)
band_p(today)       = percentile_p(normalized_range over lookback) x ATR(today)
```

## Known problems

| Problem | What it means | GTM equivalent |
|---|---|---|
| Possibly using information you would not have had at the time (look-ahead bias) | A day's ATR can include that same day's range, so the band is partly built from the result it is trying to predict | A churn model built using "support tickets in the last 30 days" counted after the customer already churned |
| Using today's unfinished numbers (current-day data leakage) | Using the values of a day that is still in progress | Lead scores that include activity logged after the opportunity was created |
| Never tested only on later days (no walk-forward backtest) | Never tested on days after the period it learned from | Checking a scoring model on the same accounts it was tuned on |
| Never checked whether its percentages match what actually happens (no calibration check) | Never checked whether the "80% band" really holds the close 80% of the time | Calling a lead "70% likely to convert" without checking that about 70% of such leads actually do |

## What a valid test would look like

1. Work out ATR using only price bars that finished before the time of the forecast.
2. Test only on days after the ones it learned from: learn the levels from a rolling window of past days, forecast the next day, move forward one day, and never use future bars.
3. Measure coverage: on what share of days did the real range fall inside each band, compared with the chance the band claims?
4. Compare it with a simple baseline (a band set at a fixed percentage) so the indicator has something to beat.

Until that is done, the indicator is a picture of past ranges, not a forecast.

## Related

- [Analytics and prediction: data leakage and calibration](../../docs/06-analytics-and-prediction/README.md)
- [Failure analysis](../../decision-examples/failure-analysis.md)
