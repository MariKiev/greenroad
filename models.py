# coding=utf-8
from app import db
from wtforms import StringField, IntegerField, TextAreaField, SelectField, PasswordField, BooleanField, ValidationError
from wtforms.validators import *
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask.ext.wtf import Form
from flask_wtf.html5 import EmailField
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

role_user = 0
role_admin = 1


class Track(db.Model):
    __tablename__ = 'track'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    length = db.Column(db.Integer)
    day = db.Column(db.Integer)
    level = db.Column(db.String)
    text = db.Column(db.String)
    route = db.Column(db.String)
    img = db.Column(db.String)

    def __init__(self, name, length, day, level, text, route, img):
        self.name = name
        self.length = length
        self.day = day
        self.level = level
        self.text = text
        self.route = route
        self.img = img

    def __repr__(self):
        return 'Track: %s, length: %s, day: %s, level: %s' % (self.name.encode('utf-8'), self.length, self.day, self.level.encode('utf-8'))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.SmallInteger, default=role_user, unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, role):
        self.role = role

    def __repr__(self):
        return 'Role %s' % self.role


class User(UserMixin, db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    remember_me = db.Column(db.Boolean)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, remember_me, role_id=0):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.remember_me = remember_me
        self.role_id = role_id

    def __repr__(self):
        return 'User: %s %s %s' % (self.username, self.email, self.role_id)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def generate_confirmation_token(self, expiration=3000):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True


class BaseRouteForm(Form):
    name = StringField(u'Название маршрута:', validators=[
        DataRequired(message=u'Заполнение данного поля обязательно'), 
        Length(min=3, max=60, message=u'Заполнение данного поля обязательно')
        ])
    length = IntegerField(u'Длина маршрута в км:', validators=[
        DataRequired(message=u'Заполнение данного поля обязательно в числовом виде'),
        NumberRange(min=1, max=None, message=u'Неверное значение')
        ])
    day = IntegerField(u'Длина маршрута в днях:', validators=[
        DataRequired(message=u'Заполнение данного поля обязательно в числовом виде'),
        NumberRange(min=1, max=None, message=u'Неверное значение')
        ])
    level = SelectField(u'Сложность маршрута:', validators=[
        AnyOf(values=[u'низкая', u'средняя', u'выше среднего', u'высокая(необходима спец. подготовка)'], 
        message=u'Неверное значение, выберите одно из следующих: %(values)s', values_formatter=None)], 
        choices=[
            (u'низкая', u'низкая'),
            (u'средняя', u'средняя'), 
            (u'выше среднего', u'выше среднего'), 
            (u'высокая (необходима спец. подготовка)', u'высокая (необходима спец. подготовка)')
        ])
    text = TextAreaField(u'Описание маршрута:', validators=[
        DataRequired(message=u'Заполнение данного поля обязательно'), 
        Length(min=300)
        ])
    route = TextAreaField(u'Ключевые точки маршрута:', validators=[
        DataRequired(message=u'Заполнение данного поля обязательно')
        ])


class AddRouteForm(BaseRouteForm):
    img = FileField(u'Загрузить фото маршрута:', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'), FileRequired()])


class EditRouteForm(BaseRouteForm):
    img = FileField(u'Загрузить фото маршрута:', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])


class RegisterForm(Form):
    name = StringField('Enter your nickname', validators=[DataRequired(message=u'Заполнение данного поля обязательно'), Length(min=1, max=20, message=u'Заполнение данного поля обязательно')])
    email = EmailField('Email address', validators=[DataRequired(message=u'Заполнение данного поля обязательно')])
    password = PasswordField('Enter your password', validators=[DataRequired(message=u'Заполнение данного поля обязательно'), Length(min=6, max=15, message=u'Введите не менее 6 символов'), EqualTo('check_password', message=u'Пароли не совпадают')])
    check_password = PasswordField('Confirm your password', validators=[DataRequired(message=u'Заполнение данного поля обязательно')])
    remember_me = BooleanField('Remember me')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class LoginForm(Form):
    email = EmailField('Email address', validators=[DataRequired(message=u'Введите ваш email')])
    password = PasswordField('Enter your password', validators=[DataRequired(message=u'Введите пароль')])
    remember_me = BooleanField('Remember me')


class ContactUsForm(Form):
    comments = TextAreaField(u'Your comments:', validators=[DataRequired(message=u'Заполнение данного поля обязательно')])
    email = EmailField('Enter your email address, please', validators=[DataRequired(message='Enter email')])