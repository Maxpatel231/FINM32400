import csv
import argparse

parser = argparse.ArgumentParser(description="Convert FIX messages to CSV")
parser.add_argument("--input_fix_file", required=True)
parser.add_argument("--output_csv_file", required=True)
args = parser.parse_args()

input_fix_file = args.input_fix_file
output_csv_file = args.output_csv_file

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
              and fields.get('39') == '2' an
