#!/usr/bin/env python
# encoding: utf-8
import json

from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'micro_flask',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)


class User(db.Document):
    name = db.StringField(max_length=50)
    email = db.StringField(required=True)

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email
        }


@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    user = User.objects(name=name).first()

    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())


@app.route('/', methods=['PUT'])
def create_records():
    record = json.loads(request.data)
    user = User(
        name=record['name'],
        email=record['email']
    )
    user.save()
    return jsonify(user.to_json())


@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(email=record['email'])


@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user.to_json())


app.run(debug=True)
