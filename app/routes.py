from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

from datetime import datetime


@app.route('/')
def show_index_page():
    users = [
        {
            'name': 'Vasya',
            'date': datetime.ctime(datetime.now()),
        },
        {
            'name': 'Sanya',
            'date': datetime.ctime(datetime(2022, 1, 25, 14, 0, 0))
        }

    ]
    return render_template('index.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def show_login_page():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"""Login requested for user {form.username.data}, 
                  user data: email - {form.user_email.data},
                             password - {form.user_password.data}        
        """)
        return redirect(url_for('show_index_page'))
    return render_template('login.html', form=form)
