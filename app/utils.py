import csv
import json
import ast
from app import mongo
import flask_pymongo


def apply_changes(original, change):
    for key in change:
        original[key] = change[key]
    return original


def remap_keys(mapping):
    return [{'object_id': k[0], 'object_type': k[1], 'history': v} for k, v in mapping.items()]


def process_csv(infile="uploads/data.csv"):
    db = mongo.db
    db.logs.drop()  # overwrite data
    logs = db.logs
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
            log = {
                'object_id': object_id,
                'object_type': object_type,
                'timestamp': timestamp,
                'object_changes': object_changes,
                'object_state': current_state,
            }
            logs.insert_one(log)
    logs.create_index([("object_id", flask_pymongo.ASCENDING),
                        ("object_type", flask_pymongo.ASCENDING)])


def get_past_state(object_type, object_id, timestamp):
    obj = mongo.db.logs.find_one({
        "object_type": object_type, 
        "object_id": object_id, 
        "timestamp": {'$lte': timestamp},
    }, sort=[("timestamp", flask_pymongo.DESCENDING)])
    return obj['object_state']

def check_data_exists():
    return mongo.db.logs.count() > 0
