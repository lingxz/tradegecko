import csv
import json
import ast
from app import db
from app.model import Log


def apply_changes(original, change):
    for key in change:
        original[key] = change[key]
    return original


def remap_keys(mapping):
    return [{'object_id': k[0], 'object_type': k[1], 'history': v} for k, v in mapping.items()]


def process_csv(infile="uploads/data.csv"):
    Log.drop_collection()  # overwrite data
    current_states = {}
    with open(infile) as f:
        next(f)  # skip the headers
        for line in f:
            items = line.split(',')
            object_id, object_type, timestamp = items[:3]
            object_id = int(object_id)
            object_type = object_type.lower()
            timestamp = int(timestamp)
            ch = ','.join(items[3:])
            object_changes = ast.literal_eval(json.loads(ch))
            key = (object_id, object_type)
            if key in current_states:
                prev_state = current_states[key]
                current_state = apply_changes(prev_state, object_changes)
            else:
                current_state = object_changes
            current_states[key] = current_state
            log = Log(object_id=object_id, object_type=object_type, timestamp=timestamp, 
                      object_changes=object_changes, object_state=current_state)
            log.save()


def get_past_state(object_type, object_id, timestamp):
    obj = Log.objects(object_type=object_type, object_id=object_id,
                      timestamp__lte=timestamp).order_by('-timestamp').limit(1).as_pymongo()[0]
    return obj['object_state']

def check_data_exists():
    return Log.objects.count() > 0
