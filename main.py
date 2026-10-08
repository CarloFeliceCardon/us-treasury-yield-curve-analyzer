import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import date as dt
from io import StringIO
from pathlib import Path

def download_yield_data(url):
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_csv(StringIO(response.text))
    df["observation_date"] = pd.to_datetime(df["observation_date"])
    return df

def add_curve_metrics(df):
    df = df.copy()
    df["slope_2s10s"]       = df["DGS10"] - df["DGS2"]
    df["slope_3m10s"]       = df["DGS10"] - df["DGS3MO"]
    df["curvature_2s5s10s"] = 2 * df["DGS5"] - df["DGS2"] - df["DGS10"]
    return df

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS1MO,DGS3MO,DGS6MO,DGS1,DGS2,DGS3,DGS5,DGS7,DGS10,DGS20,DGS30"

df = download_yield_data(url)
df = add_curve_metrics(df)

slope_2s10s_history = df[["observation_date", "slope_2s10s"]].dropna()
slope_3m10s_history = df[["observation_date", "slope_3m10s"]].dropna()
curvature_history   = df[["observation_date", "curvature_2s5s10s"]].dropna()

yield_columns = ["DGS1MO", "DGS3MO", "DGS6MO", "DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30"]
maturities_years = [1/12, 3/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30]

df_complete = df.dropna(subset = yield_columns)
latest_curve = df_complete.iloc[-1]

three_month_yield = latest_curve["DGS3MO"]
two_year_yield    = latest_curve["DGS2"]
ten_year_yield    = latest_curve["DGS10"]
five_year_yield   = latest_curve["DGS5"]

slope_2s10s       = (ten_year_yield - two_year_yield).round(4)
slope_3m10s       = (ten_year_yield - three_month_yield).round(4)
curvature_2s5s10s = (2 * five_year_yield - two_year_yield - ten_year_yield).round(4)

curve_data = pd.DataFrame(
    {
        "maturity_years" : maturities_years,
        "yield_percent"  : latest_curve[yield_columns].values
    }
)

output_dir = Path("output")
output_dir.mkdir(exist_ok = True)

print(f"2s10s slope: {slope_2s10s}")
print(f"3m10s slope: {slope_3m10s}")
print(f"2s5s10s curvature: {curvature_2s5s10s}")

if slope_2s10s < 0:
    print("The 2s10s curve is inverted")
else:
    print("The 2s10s curve is normal")

# Yield Curve Chart
plt.figure(figsize = (10,6))
plt.plot(
    curve_data["maturity_years"],
    curve_data["yield_percent"],
    marker = "o"
)
plt.title(f"{dt.today()} Yield Curve")
plt.xlabel("Maturity")
plt.ylabel("Yield (%)")
plt.grid(True)
plt.savefig(
    output_dir / "current_yield_curve.png",
    dpi = 300,
    bbox_inches = "tight"
)

# 2s10s Slope Chart
plt.figure(figsize = (10, 6))
plt.plot(
    slope_2s10s_history["observation_date"],
    slope_2s10s_history["slope_2s10s"],
    color = "navy"
)
plt.axhline(
    y         = 0,
    color     = "red",
    linestyle = "--"
)
plt.fill_between(
    slope_2s10s_history["observation_date"],
    slope_2s10s_history["slope_2s10s"],
    0,
    where = slope_2s10s_history["slope_2s10s"] < 0,
    color = "red",
    alpha = 0.25,
    label = "Inverted"
)
plt.title("US Treasury 2s10s Slope")
plt.xlabel("Date")
plt.ylabel("Percentage Points")
plt.legend()
plt.savefig(
    output_dir / "slope_2s10s_history.png",
    dpi = 300,
    bbox_inches = "tight"
)

# 3m10s Slope Chart
plt.figure(figsize = (10, 6))
plt.plot(
    slope_3m10s_history["observation_date"],
    slope_3m10s_history["slope_3m10s"],
    color = "navy"
)
plt.axhline(
    y         = 0,
    color     = "red",
    linestyle = "--"
)
plt.fill_between(
    slope_3m10s_history["observation_date"],
    slope_3m10s_history["slope_3m10s"],
    0,
    where = slope_3m10s_history["slope_3m10s"] < 0,
    color = "red",
    alpha = 0.25,
    label = "Inverted"
)
plt.title("US Treasury 3m10s Slope")
plt.xlabel("Date")
plt.ylabel("Percentage Points")
plt.legend()
plt.savefig(
    output_dir / "slope_3m10s_history.png",
    dpi = 300,
    bbox_inches = "tight"
)

# Curvature Chart
plt.figure(figsize=(10, 6))
plt.plot(
    curvature_history["observation_date"],
    curvature_history["curvature_2s5s10s"],
    color = "navy"
)
plt.axhline(
    y         = 0,
    color     = "darkgreen",
    linestyle = "--"
)
plt.title("US Treasury 2s5s10s Curvature")
plt.xlabel("Date")
plt.ylabel("Percentage Points")
plt.savefig(
    output_dir / "curvature_2s5s10s_history.png",
    dpi = 300,
    bbox_inches = "tight"
)

plt.show()