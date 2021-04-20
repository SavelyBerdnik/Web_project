from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify, render_template, redirect
from data import news_resources, db_session
from data.users import User
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
db_session.global_init("db/main.db")
session = db_session.create_session()


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['username'] = "Ученик Яндекс.Лицея"
    param['title'] = 'Домашняя страница'
    return render_template('index.html', **param)


@app.route('/quest')
def quest():
    return render_template('quest.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = session.query(User)
        if users.filter(User.email == form.email and
                        User.login == form.username and
                        User.password == form.password):
            return redirect('/index')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        users = session.query(User)
        if not (users.filter(User.email == form.email) and
                users.filter(User.login == form.username) and
                users.filter(User.password == form.password)):
            user = User()
            user.login = form.username
            user.email = form.email
            user.password = form.password
            session.add(user)
            session.commit()

        return redirect('/index')
    return render_template('registration.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run()
