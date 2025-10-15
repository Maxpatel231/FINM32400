import pandas as pd

input_csv_file = "orders.csv"
output_metrics_file = "metrics.csv"

df = pd.read_csv(input_csv_file)

df['OrderTransactTime'] = pd.to_datetime(df['OrderTransactTime'])
df['ExecutionTransactTime'] = pd.to_datetime(df['ExecutionTransactTime'])
df['ExecSpeedSecs'] = (df['ExecutionTransactTime'] - df['OrderTransactTime']).dt.total_seconds()

df['LimitPrice'] = df['LimitPrice'].astype(float)
df['AvgPx'] = df['AvgPx'].astype(float)
df['Side'] = df['Side'].astype(int)

def price_improvement(row):
    if row['Side'] == 1:
        val = row['LimitPrice'] - row['AvgPx']
    else:
        val = row['AvgPx'] - row['LimitPrice']
    return max(val, 0)

df['PriceImprovement'] = df.apply(price_improvement, axis=1)

metrics = df.groupby('LastMkt').agg(
    AvgPriceImprovement=('PriceImprovement','mean'),
    AvgExecSpeedSecs=('ExecSpeedSecs','mean')
).reset_index()

metrics.to_csv(output_metrics_file, index=False)
print('✅ Metrics saved to', output_metrics_file)