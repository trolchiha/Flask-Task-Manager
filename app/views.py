from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    user_id=current_user.id
    tasks = Task.query.filter_by(user_id=user_id).all()
    
    return render_template('tasks.html', title="Tasks", tasks=tasks)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()

    if request.method == "POST":
        new_username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        old_password = user.password

        if not password:
            if check_username(user.username, new_username):
                user.username = new_username
                db.session.commit()
                flash('Profile updated!', category='success')
            return redirect(url_for('views.profile'))
        elif check_password(password, new_password, old_password) and check_username(user.username, new_username):
            user.username = new_username
            user.password = generate_password_hash(new_password)
            db.session.commit()

            flash('Profile updated!', category='success')
            return redirect(url_for('views.profile'))
        
        
    return render_template('profile.html', title="Profile", user=user)

@views.route('/profile-delete/<int:user_id>')
@login_required
def delete_profile(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Your profile was deleted!', category='success')
    return redirect(url_for('auth.sign_up'))

@views.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        task.data = request.form['data']
        db.session.commit()

    return render_template('update-task.html', title="Task", task=task)


@views.route('/task-delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Your task was deleted!', category='success')
    return redirect(url_for('views.home'))

def check_password(password, new_password, old_password):
    
    if not check_password_hash(old_password, password):
        flash('Password is wrong', category='error')
        return False
    elif len(new_password) < 7:
        flash('Password must be at least 7 characters.', category='error')
        return False

    return True

def check_username(username, new_username):
    if username != new_username:
        user = User.query.filter_by(username=new_username).first()
    else:
        user = None
    
    if user:
        flash('User with such username already exists.', category='error')
        return False

    elif len(username) < 4:
        flash('Username must be greater than 3 characters.', category='error')
        return False

    return True
