from flask import request
from flask_restful import Resource
from app.models import *
from .schemas import *
from . import api 

class UsersListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)
    
    def post(self):
        new_user = User(
            username=request.json['username'],
            password=request.json['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

api.add_resource(UsersListResource, '/users')
api.add_resource(UserResource, '/user/<int:user_id>')