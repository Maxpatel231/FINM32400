import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Calculate per-exchange execution metrics")
parser.add_argument("--input_csv_file", required=True, help="Path to CSV produced by fix_to_csv.py")
parser.add_argument("--output_metrics_file", required=True, help="Path to output metrics CSV")
args = parser.parse_args()

input_csv_file = args.input_csv_file
output_metrics_file = args.output_metrics_file

df = pd.read_csv(input_csv_file)

df['OrderTransactTime'] = pd.to_datetime(df['OrderTransactTime'])
df['ExecutionTransactTime'] = pd.to_datetime(df['ExecutionTransactTime'])
df['ExecSpeedSecs'] = (df['ExecutionTransactTime'] - df['OrderTransactTime']).dt.total_seconds()

df['LimitPrice'] = df['LimitPrice'].astype(float)
df['AvgPx'] = df['AvgPx'].astype(float)
df['Side'] = df['Side'].astype(int)

def price_improvement(row):
    # Side 1 = Buy → improvement if AvgPx < LimitPrice
    # Side 2 = Sell → improvement if AvgPx > LimitPrice
    if row['Side'] == 1:
        val = row['LimitPrice'] - row['AvgPx']
    else:
        val = row['AvgPx'] - row['LimitPrice']
    return max(val, 0)

df['PriceImprovement'] = df.apply(price_improvement, axis=1)

metrics = df.groupby('LastMkt').agg(
    AvgPriceImprovement=('PriceImprovement', 'mean'),
    AvgExecSpeedSecs=('ExecSpeedSecs', 'mean')
).reset_index()

metrics.to_csv(output_metrics_file, index=False)
print(f"✅ Metrics saved to {output_metrics_file}")
