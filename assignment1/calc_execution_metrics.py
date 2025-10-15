import csv

def parse_fix_line(line):
    if '\x01' not in line:
        line = line.replace('^A', '\x01')
    parts = line.split('\x01')
    fields = {}
    for p in parts:
        if '=' in p:
            tag, value = p.split('=', 1)
            fields[tag] = value
    return fields

input_fix_file = "cleaned.fix"
output_csv_file = "orders.csv"

orders = {}
fills = []

with open(input_fix_file, 'r', encoding='utf-8') as f:
    for raw_line in f:
        if ':' not in raw_line:
            continue
        _, fix_part = raw_line.split(':', 1)
        fields = parse_fix_line(fix_part.strip())

        msg_type = fields.get('35')
        if msg_type == 'D':
            orders[fields['11']] = fields
        elif (msg_type == '8' and fields.get('150') == '2'
              and fields.get('39') == '2' and fields.get('40') == '2'):
            clid = fields.get('11')
            if clid in orders:
                order = orders[clid]
                fills.append({
                    'OrderID': clid,
                    'OrderTransactTime': order.get('60', ''),
                    'ExecutionTransactTime': fields.get('60', ''),
                    'Symbol': fields.get('55', ''),
                    'Side': fields.get('54', ''),
                    'OrderQty': fields.get('38', ''),
                    'LimitPrice': fields.get('44', ''),
                    'AvgPx': fields.get('6', ''),
                    'LastMkt': fields.get('30', ''),
                })

with open(output_csv_file, 'w', newline='') as out_f:
    writer = csv.DictWriter(out_f, fieldnames=[
        'OrderID','OrderTransactTime','ExecutionTransactTime','Symbol',
        'Side','OrderQty','LimitPrice','AvgPx','LastMkt'
    ])
    writer.writeheader()
    writer.writerows(fills)

print(f"✅ Done! Wrote {len(fills)} fills to {output_csv_file}")
