#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
args = parser.parse_args()


# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

data = counts[args.key]

top_items = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
top_items_sorted = sorted(top_items, key=lambda x: x[1])
keys, values = zip(*top_items_sorted)

plt.figure(figsize=(10, 6))
plt.bar(keys, values, color='skyblue')
plt.xlabel('Keys')
plt.ylabel('Counts')
plt.title(f'Bar Chart for {args.key}')
plt.xticks(rotation=45)
plt.tight_layout()

basename = os.path.basename(args.input_path)

basename = os.path.splitext(basename)[0]

output_filename = f"{os.path.basename(args.input_path)}_{args.key.replace('#','')}.png"
#output_filename = f"{basename}_{args.key}.png"
plt.savefig(output_filename)
print(f"Plot saved as {output_filename}")
