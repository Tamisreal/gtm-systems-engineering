# SPX probabilistic range study

**Evidence status: Exploratory Research.** Not a validated model. No predictive accuracy is claimed.

This sits outside the GTM projects on purpose. It is here because the way it fails is instructive for anyone building scores or forecasts on GTM data: the same leakage that makes a trading indicator look accurate makes a churn model or a lead score look accurate.

## What it is

A TradingView Pine Script indicator that projects a likely intraday range for the S&P 500 index. It normalizes historical daily ranges by Average True Range (ATR), takes empirical percentiles of those normalized ranges, and scales them by the current ATR to draw probability bands.

```
normalized_range(d) = (high(d) - low(d)) / ATR(d)
band_p(today)       = percentile_p(normalized_range over lookback) x ATR(today)
```

## Known problems

| Problem | What it means | GTM equivalent |
|---|---|---|
| Possible look-ahead bias | ATR for a day can include that day's own range, so the band is partly built from the outcome it predicts | A churn model trained with "support tickets in the last 30 days" measured after the churn date |
| Current-day data leakage | Using the in-progress day's values during the day | Lead scores that include activity logged after the opportunity was created |
| No walk-forward backtest | Never tested on data strictly after the period used to fit it | Validating a scoring model on the same accounts it was tuned on |
| No calibration check | Never checked whether the "80% band" contains the close 80% of the time | Calling a lead "70% likely to convert" without a reliability check |

## What a valid test would look like

1. Compute ATR using only bars that closed before the forecast time.
2. Walk forward: fit percentiles on a rolling window, forecast the next day, roll forward, never touch future bars.
3. Measure coverage: the share of days the realized range fell inside each band, against the band's nominal probability.
4. Compare with a naive baseline (fixed-percentage band) so the indicator has something to beat.

Until that is done, the indicator is a visualization of historical ranges, not a forecast.

## Related

- [Analytics and prediction: data leakage and calibration](../../docs/06-analytics-and-prediction/README.md)
- [Failure analysis](../../decision-examples/failure-analysis.md)
