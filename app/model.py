from app import db

class Log(db.Document):

    object_id = db.IntField(required=True)
    object_type = db.StringField(required=True)
    timestamp = db.IntField(required=True)
    object_changes = db.DynamicField(required=True)
    object_state = db.DynamicField(required=True)

    meta = {
        'indexes': [
             {'fields': ('object_id', 'object_type')},
             'timestamp'
        ]
    }
