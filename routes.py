from datetime import datetime

from werkzeug.security import check_password_hash
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from flask import jsonify, request
from flask_validator import ValidateEmail, ValidateLength
from flask_httpauth import HTTPBasicAuth

from ads import app, db
from models import Ads, User

auth = HTTPBasicAuth()

validator_email = ValidateEmail(field=User.email, throw_exception=True,
                                message='Неверный формат адреса электронной почты')

validator_title_len = ValidateLength(field=Ads.title, throw_exception=True, min_length=2,
                    max_length=30,
                    message="Параметр 'title' минимум 2 символа, максимум - 30 символов")

validator_descr_len = ValidateLength(field=Ads.description, throw_exception=True, min_length=2,
                    max_length=100,
                    message="Параметр 'description' минимум 2 символа, максимум - 100 символов")

validator_username_field = ValidateLength(field=User.username, throw_exception=True,
                    min_length=2, max_length=15,
                    message="параметр 'username' минимум 2 символа, максимум - 15 символов")


@app.route('/api/v1.0/ads/<ID>',  methods=['GET'])  # возвращает одно объявление
def get(ID):
    ads = Ads.query.get_or_404(ID).description
    return jsonify({'Содержание объявления': ads})


@app.route('/api/v1.0/ads',  methods=['GET'])  # возвращает все объявления
def get_all():
    ads = Ads.query.all()
    ads_list = [x.title for x in ads]
    return jsonify({'Список объявлений': ads_list})



@app.route('/api/v1.0/ads',  methods=['POST'])  # добавляет новое объявление
@auth.login_required
def post():
    try:
        user = auth.username()
        user_id = User.query.filter_by(username=user).first().id
        title = request.args.to_dict()['title']
        description = request.args.to_dict()['description']
        create_date = f'{datetime.now()}'

        if validator_title_len.check_value(title) and\
        validator_descr_len.check_value(description):
            ad = Ads(title=title, description=description, create_date=create_date, user_id=user_id)
            db.session.add(ad)
            db.session.commit()
            return jsonify({'status': 'OK. Объявление успешно добавлено!'})
        elif not validator_title_len.check_value(title):
            return jsonify({'status': validator_title_len.message}), 400
        elif not validator_descr_len.check_value(description):
            return jsonify({'status': validator_descr_len.message}), 400
    except KeyError as ke:
        return jsonify({'Необходимо добавить параметр': f'{ke}'}), 400


@app.route('/api/v1.0/ads/<ID>',  methods=['DELETE'])  # удаляет одно объявление
@auth.login_required
def delete(ID):
    current_user_id = User.query.filter_by(username=auth.current_user()).first().id
    ads = Ads.query.get_or_404(ID)
    if ads.user_id == current_user_id:
        db.session.delete(ads)
        db.session.commit()
        return jsonify({'Удалено': ads.title})
    else:
        return jsonify({'Status': 'Не удалено! Это может сделать только автор объявления'}), 400


@app.route('/api/v1.0/ads/<ID>',  methods=['PATCH'])  # изменяет одно объявление
@auth.login_required
def edit(ID):
    current_user_id = User.query.filter_by(username=auth.current_user()).first().id
    ads = Ads.query.get_or_404(ID)
    if ads.user_id == current_user_id:
        if "title" in request.args.to_dict().keys():
            ads.title = request.args.to_dict()['title']
        if "description" in request.args.to_dict().keys():
            ads.description = request.args.to_dict()['description']
        db.session.commit()
        return jsonify({'Обновлено': ads.title})
    else:
        return jsonify({'Status': 'Не изменено! Это может сделать только автор объявления'}), 400



@app.route('/api/v1.0/users', methods=['POST'])    #добавляет нового пользователя
def new_user():
    username = request.args.get('username')
    if not validator_username_field.check_value(username):
        return jsonify({'Ошибка': validator_username_field.message}), 400
    password = request.args.get('password')
    if len(password) < 8:
        return jsonify({'Ошибка': "параметр 'password' должен быть минимум 8 символов"}), 400
    email = request.args.get('email')
    if not validator_email.check_value(email):
        return jsonify({'Ошибка': validator_email.message}), 400
    if username is None or password is None or email is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.password_hash = generate_password_hash(password)
    user.email = email
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201


@auth.verify_password
def verify_password(username, password):
    users = User.query.all()
    users_list = [x.username for x in users]
    if username in users_list and\
    check_password_hash(User.query.filter_by(username=username).first().password_hash, password):
        return username
