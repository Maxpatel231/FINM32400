import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Calculate exchange metrics")
parser.add_argument("--input_csv_file", required=True)
parser.add_argument("--output_metrics_file", required=True)
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
    if row['Side'] == 1:  # Buy order
        val = row['LimitPrice'] - row['AvgPx']
    else:  # Sell order
        val = row['AvgPx'] - row['LimitPrice']
    return max(val, 0)

df['PriceImprovement'] = df.apply(price_improvement, axis=1)

metrics = df.groupby('LastMkt').agg(
    AvgPriceImprovement=('PriceImprovement', 'mean'),
    AvgExecSpeedSecs=('ExecSpeedSecs', 'mean')
).reset_index()

metrics.to_csv(output_metrics_file, index=False)
print('✅ Metrics saved to', output_metrics_file)
