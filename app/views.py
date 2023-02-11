from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import *

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    user_id=current_user.id
    tasks = Task.query.filter_by(user_id=user_id).all()
    
    return render_template('tasks.html', title="Tasks", tasks=tasks)
