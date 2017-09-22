import csv
import json
import ast
from collections import defaultdict

def apply_changes(original, change):
    for key in change:
        original[key] = change[key]
    return original

def remap_keys(mapping):
    return [{'object_id':k[0], 'object_type': k[1],'history': v} for k, v in mapping.items()]

def process_csv(infile="uploads/data.csv", outfile="out.json"):
    data = defaultdict(list)
    with open(infile) as f:
        next(f)  # skip the headers
        for line in f:
            items = line.split(',')
            object_id, object_type, timestamp = items[:3]
            object_id = int(object_id)
            timestamp = int(timestamp)
            ch = ','.join(items[3:])
            object_changes = ast.literal_eval(json.loads(ch))
            data[(object_id, object_type)].append((timestamp, object_changes))

    state_dict = defaultdict(list)  # variable storing the state of object at each timestamp
    for key in data:
        sorted_changes = sorted(data[key], key=lambda x:x[0])  # sort changes by timestamp
        current_state = None
        for c in sorted_changes:
            timestamp, change = c
            if not current_state:
                current_state = change
            else:
                current_state = apply_changes(current_state, change)
            state_dict[key].append((timestamp, current_state))
    with open(outfile, 'w') as f:
        json.dump(remap_keys(state_dict), f, indent=2)
