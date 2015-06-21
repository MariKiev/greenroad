# coding=utf-8
import time
import os.path
import json
from PIL import Image
from flask import render_template, request, flash, redirect, url_for
from flask.ext.login import login_required

from app import app, login_manager, basedir
from models import *
from settings import IMAGE_MAXSIZEX, IMAGE_MAXSIZEY, POST_PER_PAGE
from mail import render_email, send_email


@app.route('/')
def index():
    tracks = Track.query.order_by(Track.id.desc()).limit(3).all()
    return render_template('home.html', tracks=tracks)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # args = (form.name.data, form.email.data, form.password.data, form.remember_me.data)
        # user = User(*args)  # распаковка
        user = User(form.name.data, form.email.data, form.password.data, form.remember_me.data)

        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        text, html = render_email('/email/confirm', user=user, token=token)
        send_email(user.email, 'Confirm your account', html, text)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        flash('You have confirmed you account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Hello, {}' .format(user.username))
            return redirect(request.args.get('next') or url_for('index'))
        flash(u'Неверный email или пароль.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/routes')
def routes():
    page = request.args.get('page', 1, type=int)
    pagination = Track.query.order_by(Track.id.asc()).paginate(page, per_page=POST_PER_PAGE, error_out=False)
    tracks = pagination.items
    return render_template('routes.html', tracks=tracks, pagination=pagination, ajax=request.is_xhr)


@app.route('/add_route', methods=['GET', 'POST'])
@login_required
def add_route2():
    form = AddRouteForm()
    if request.is_xhr:
        del form.img
        if form.validate_on_submit():
            return json.dumps({})
        else:
            return json.dumps(form.errors)
    if form.validate_on_submit():
        img = request.files['img']
        subpath = os.path.join('static/img', str(time.time()) + '.jpg')
        filename = os.path.join(basedir, subpath)
        img.save(filename)

        with Image.open(filename) as im:
            (width, height) = im.size

            new_filename = 'static/img_360x250/' + str(time.time()) + '.jpg'
            im = im.resize((IMAGE_MAXSIZEX, IMAGE_MAXSIZEY), Image.ANTIALIAS)
            im.save(basedir + '/' + new_filename, "jpeg", quality=100)

        track_img = '/' + new_filename
        track = Track(form.name.data, form.length.data, form.day.data, form.level.data, form.text.data, form.route.data,
                      track_img)
        db.session.add(track)
        db.session.commit()
        flash('Your post was published!')
        return redirect(url_for('route', track_id=track.id))
    return render_template('add_route2.html', form=form)


@app.route('/edit_route/<track_id>/', methods=['GET', 'POST'])
def edit_route2(track_id):
    track = Track.query.get_or_404(track_id)
    form = EditRouteForm(obj=track)
    if request.is_xhr:
        if form.validate_on_submit():
            return json.dumps({})
        else:
            return json.dumps(form.errors)
    if form.validate_on_submit():
        track.name = form.name.data
        track.length = form.length.data
        track.day = form.day.data
        track.level = form.level.data
        track.text = form.text.data
        track.route = form.route.data
        if form.img.data:
            img = request.files['img']
            subpath = os.path.join('static/img', str(time.time()) + '.jpg')
            filename = os.path.join(basedir, subpath)
            img.save(filename)

            with Image.open(filename) as im:

                im = im.resize((IMAGE_MAXSIZEX, IMAGE_MAXSIZEY), Image.ANTIALIAS)
                new_filename = 'static/img_360x250/' + str(time.time()) + '.jpg'
                im.save(basedir + '/' + new_filename, "jpeg", quality=100)

            track.img = '/' + new_filename
        db.session.commit()
        flash('Your post was edited!')
        return redirect(url_for('route', track_id=track.id))
    return render_template('edit_route2.html', form=form, track_id=track.id)


@app.route('/route/<int:track_id>/')
def route(track_id):
    track = Track.query.get_or_404(track_id)
    return render_template('route.html', track=track)


@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = ContactUsForm()
    if request.is_xhr:
        if form.validate_on_submit():
            return json.dumps({})
        else:
            return json.dumps(form.errors)

    if form.validate_on_submit():
        comments = form.comments.data
        email = form.email.data
        _, html = render_email('/email/feedback', comments=comments, email=email)
        send_email('iam.marik@gmail.com', 'Feedback from site Green road', html)
        flash('Your massage was sent!')
        return redirect(url_for('index'))
    return render_template('contact_us.html', form=form)