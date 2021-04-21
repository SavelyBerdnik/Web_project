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
    submit = SubmitField('Зарегистрироваться')


class InputForm(FlaskForm):
    code = StringField('Введите код', validators=[DataRequired()])
    submit = SubmitField('Перейти')


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = session.query(User)
        if users.filter(User.email == form.email and
                        User.login == form.username and
                        User.password == form.password):
            return redirect('/create')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        users = session.query(User)
        if not (users.filter(User.email == form.email or User.login == form.username)):
            user = User()
            user.login = form.username
            user.email = form.email
            user.password = form.password
            session.add(user)
            session.commit()

        return redirect('/create')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/code_input', methods=['GET', 'POST'])
def code_input():
    form = InputForm()
    if form.validate_on_submit():
        return redirect('/create')
    return render_template('code_input.html', title='Ввод кода', form=form)


@app.route('/quest')
def quest():
    return render_template('quest.html')


@app.route('/create')
def create():
    return render_template('create.html')


if __name__ == '__main__':
    app.run()
