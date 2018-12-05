import logging
from datetime import datetime

from flask_login import current_user, login_user, logout_user, login_required

from dao import db
from models.User import User, Post
from webapp import app
from flask import render_template, redirect, url_for, flash

from webapp.Froms import LoginForm, RegisterForm, editProfileForm, postForm


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # 在使用 current_user 时user对象已被加载到session 中
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template('error.html', errMsg='Invalid username or password')
        login_user(user, remember=form.remember.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form, title='sign in')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(id=5, username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='sign up', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_name=username).all()
    form = editProfileForm()
    postform = postForm()
    # 只是通过HTTP方法是否是“PUT”或“POST”来判断
    if postform.submit.data and postform.validate_on_submit():
        post = Post(body=postform.post.data, timestamp=datetime.utcnow(), user_name=current_user.username,
                    user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user', username=username))

    if form.submitupdate.data and form.validate_on_submit():
        current_user.about_me = form.about_me.data
        flash('edit success!')
        db.session.add(current_user)
        db.session.commit()
        app.logger.info('user %s modify about', current_user.username)
        return redirect(url_for('user', username=username))

    return render_template('user.html', user=user, posts=posts, form=form, postform=postform)
