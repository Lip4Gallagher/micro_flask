#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Flask, request, jsonify
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'micro_flask',
    'host': 'localhost',
    'port': 27017
}
app.secret_key = 'youdontknowme'

db = MongoEngine()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


@app.route('/login', methods=['POST'])
def login():
    info = json.loads(request.data)
    username = info.get('username', 'guest')
    password = info.get('password', '')

    user = User.objects(name=username, password=password).first()
    if user:
        login_user(user)
        return jsonify(user.to_json())
    else:
        return jsonify(
            {
                'status': 401,
                'reason': 'Username or Password Error'
            }
        )


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(**{'result': 200, 'data': {'message': 'logout success'}})


@app.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        resp = {"result": 200, "data": current_user.to_json()}
    else:
        resp = {"result": 401, "data": {"message": "user no login"}}
    return jsonify(**resp)


class Permission():
    READ = 0x01
    CREATE = 0x02
    UPDATE = 0x04
    DELETE = 0x08
    DEFAULT = READ


class Role(db.Document):
    name = db.StringField()
    permission = db.IntField()


class User(db.Document):
    name = db.StringField(max_length=50)
    password = db.StringField(max_length=30)
    email = db.StringField(required=True)
    role = db.ReferenceField('Role', default=DEFAULT_ROLE)

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@app.route('/', methods=['GET'])
@login_required
def query_records():
    name = request.args.get('name')
    user = User.objects(name=name).first()

    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())


@app.route('/', methods=['PUT'])
@login_required
def create_records():
    record = json.loads(request.data)
    user = User(
        name=record['name'],
        email=record['email']
    )
    user.save()
    return jsonify(user.to_json())


@app.route('/', methods=['POST'])
@login_required
def update_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(email=record['email'])


@app.route('/', methods=['DELETE'])
@login_required
def delete_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user.to_json())


if __name__ == '__main__':
    app.run(debug=True)
