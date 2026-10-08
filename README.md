# U.S. Treasury Yield Curve Analyzer

Python project that downloads U.S. Treasury constant-maturity yield data, analyses the current yield curve, and produces historical charts for key curve metrics.

## Features

- Downloads daily Treasury yield data from FRED
- Builds and plots the latest available yield curve
- Calculates the 2s10s and 3m10s slopes
- Identifies inversions in the historical slope series
- Calculates the 2s5s10s curvature
- Saves charts as PNG files in the `output` folder

## Data source

FRED daily Treasury constant-maturity yield series:

- DGS1MO, DGS3MO, DGS6MO
- DGS1, DGS2, DGS3, DGS5, DGS7, DGS10, DGS20, DGS30

## Metrics

- **2s10s:** 10-year yield minus 2-year yield
- **3m10s:** 10-year yield minus 3-month yield
- **2s5s10s curvature:** 2 × 5-year yield − 2-year yield − 10-year yield

## Requirements

- Python 3
- pandas
- matplotlib
- requests

## Run

Activate the project environment:

```bash
source .venv/bin/activate