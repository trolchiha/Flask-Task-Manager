from app import ma 

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "data", "status", "user_id")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
