from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreatePostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse

from datetime import datetime


@app.route('/')
@login_required
def show_index_page():
    users = list(User.query.all())
    return render_template('index.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def show_login_page():
    if current_user.is_authenticated:
        return redirect(url_for('show_index_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.user_password.data):
            flash('Invalid username or password')
            return redirect(url_for('show_login_page'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('show_index_page')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('show_index_page'))


@app.route('/registration', methods=['GET', 'POST'])
def show_registry_page():
    if current_user.is_authenticated:
        return redirect(url_for('show_index_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.user_email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are registered')
        return redirect(url_for('show_index_page'))
    return render_template('registary.html', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def show_user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    posts_count = len(posts)
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.post_content.data)
        post.author = user
        db.session.add(post)
        db.session.commit()
        flash('Your post has been published')
        return redirect(url_for('show_user_profile', username=user.username))
    return render_template('user_detail.html', user=user, posts=posts, posts_count=posts_count, form=form)


@app.route('/post/<post_id>')
@login_required
def show_post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)
