import csv
import json
import ast
import os
import copy
from app import mongo, constants, PoolHandler
from pymongo import MongoClient
import flask_pymongo


def apply_changes(original, change):
    prev = copy.deepcopy(original)
    for key in change:
        prev[key] = change[key]
    return prev


def remap_keys(mapping):
    return [{'object_id': k[0], 'object_type': k[1], 'history': v} for k, v in mapping.items()]


def process_csv(infile="uploads/data.csv"):
    db = mongo.db
    db.logs.drop()  # overwrite data
    logs = db.logs
    current_states = {}

    pool_handler = PoolHandler()
    q = pool_handler.q
    pool = pool_handler.pool
    watcher = pool.apply_async(queue_reader, (q, db.name))

    logs.create_index([("object_id", flask_pymongo.ASCENDING),
                    ("object_type", flask_pymongo.ASCENDING),
                    ("timestamp", flask_pymongo.DESCENDING)], background=True)

    if os.stat(infile).st_size == 0:
        raise IOError("File is empty")
    with open(infile) as f:
        try:
            next(f)  # skip the headers
        except StopIteration:
            raise ValueError("File is only one line wrong")
        buffer_logs = []
        count = 0
        for line in f:
            items = line.split(',')
            if len(items) < 4:
                raise IOError("Data is malformed, number of fields is less than 3")
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
            buffer_logs.append(log)  # bulk insert to speed up db calls
            count += 1
            if count == 2500:
                q.put(buffer_logs)
                buffer_logs = []
                count = 0

    if buffer_logs:
        q.put(buffer_logs)
        buffer_logs = []
    q.put('DONE')
    watcher.get()


def queue_reader(q, db_name):
    mongo = MongoClient(constants.MONGO_HOST, constants.MONGO_PORT)
    logs = mongo[db_name].logs
    while True:
        chunk = q.get()
        if chunk == 'DONE':
            break
        logs.insert_many(chunk, ordered=False)


def get_past_state(object_type, object_id, timestamp):
    obj = mongo.db.logs.find_one({
        "object_type": object_type, 
        "object_id": object_id, 
        "timestamp": {'$lte': timestamp},
    }, sort=[("timestamp", flask_pymongo.DESCENDING)])
    print(obj)
    return obj

def check_data_exists():
    return mongo.db.logs.count() > 0
