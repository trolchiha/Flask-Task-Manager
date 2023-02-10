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

        try:
            db.session.add(new_user)
            db.session.commit()
            return user_schema.dump(new_user)
        except:
            return 404

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        user.username=request.json['username']
        user.password=request.json['password']

        try:
            db.session.commit()
            return user_schema.dump(user)    
        except:
            return 404

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
            return 204
        except:
            return 404

api.add_resource(UsersListResource, '/users')
api.add_resource(UserResource, '/user/<int:user_id>')

class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)

    def post(self):
        new_task = Task(
            data=request.json['data'],
            user_id=request.json['user_id'],
        )
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return task_schema.dump(new_task)
        except:
            return 404

class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return task_schema.dump(task)

    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        task.data=request.json['data']
        task.status=request.json['status']
        task.user_id=request.json['user_id']

        try:
            db.session.commit()
            return task_schema.dump(task)    
        except:
            return 404

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)

        try:
            db.session.delete(task)
            db.session.commit()
            return 204
        except:
            return 404      

api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/task/<int:task_id>')
