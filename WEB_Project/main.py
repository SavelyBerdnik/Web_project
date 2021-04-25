from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, request, jsonify, render_template, redirect
from data import news_resources, db_session
from data.users import User
import json
from data.forms import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
db_session.global_init("db/main.db")
session = db_session.create_session()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if session.query(User).filter(User.email == form.email and
                                      User.login == form.username and
                                      User.password == form.password):
            return redirect('/main_page')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        if len(list(session.query(User).filter(User.email == form.email or User.login == form.username))) == 0:
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


@app.route('/page_name')


@app.route('/quest')
def quest():
    return render_template('quest.html')


@app.route('/main_page')
def main_page():
    if request.method == 'POST':
        select = request.form.get('method_cipher')
        if select == 'open_form':
            pass
        else:
            return redirect('/create_quest')
    return render_template('main_page.html')


if __name__ == '__main__':
    app.run()
