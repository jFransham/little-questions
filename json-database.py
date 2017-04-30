# Uses flask because I don't know how to make a simple non-static-file server
# in SimpleHTTPServer and I don't have time to learn. Sorry.
from flask import Flask, request, abort
import json

current_id = 0
# NOTE: We use string keys for the database to simplify serializing to/from
#       JSON.
database = dict()
database_save_path = 'database.json'


def serialize():
    with open(database_save_path, 'w') as db_file:
        json.dump(database, db_file)


def deserialize():
    global database, current_id

    try:
        with open(database_save_path) as db_file:
            database = json.load(db_file)
            current_id = max(map(int, database.keys())) + 1
    except FileNotFoundError:
        pass


def add_to_database(obj):
    global current_id, database

    new_id = current_id
    current_id += 1

    database[str(new_id)] = obj

    return (new_id, obj)


def get_from_database(i):
    return database.get(str(i))


def update_database(i, obj):
    current = database.get(str(i))

    if current is None:
        return None

    for (k, v) in obj.items():
        current[k] = v

    return current


def delete_from_database(i):
    existing = database.get(str(i))
    if existing is None:
        return None
    else:
        del database[str(i)]
        return existing


app = Flask(__name__)


@app.route('/<int:element_id>', methods=['GET'])
def app_get(element_id):
    out = get_from_database(element_id)
    if out is None:
        abort(400)
    return json.dumps(out)


@app.route('/', methods=['POST'])
def app_post():
    if not request.json:
        abort(400)

    value = request.json
    (new_id, value) = add_to_database(value)
    out_val = dict(value)
    out_val['id'] = new_id

    serialize()
    return json.dumps(out_val)


@app.route('/', methods=['PUT'])
def app_put():
    if not request.json:
        abort(400)

    value = request.json
    val_id = value.get('id')
    if val_id is None:
        abort(400)
    new_val = update_database(val_id, value)
    if new_val is None:
        abort(400)

    serialize()
    return json.dumps(new_val)


@app.route('/<int:element_id>', methods=['DELETE'])
def app_delete(element_id):
    if not request.json:
        abort(400)

    deleted = delete_from_database(element_id)
    if deleted is None:
        abort(400)

    serialize()
    return json.dumps(deleted)


deserialize()
app.run(port=8080)
