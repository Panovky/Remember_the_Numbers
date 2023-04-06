from app import app, db
from flask import render_template, request, redirect, make_response
from .models import Gamer, Session, Level, NumbersList, AnswersList
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint


@app.route('/')
def go_to_authorization_page():
    return redirect('/authorization')


@app.route('/authorization')
def show_authorization_page():
    return render_template('/authorization.html')


@app.route('/authorization/sign-in', methods=['post', 'get'])
def sign_in():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        gamer = db.session.query(Gamer).filter(Gamer.login == login).first()

        if gamer is not None and check_password_hash(gamer.password_hash, password):
            response = make_response(redirect('/personal_area'))
            response.set_cookie('gamer_id', str(gamer.id), max_age=None)
            return response
        else:
            return render_template('/sign_in.html', message="неверный логин или пароль")
    else:
        return render_template('/sign_in.html')


@app.route('/authorization/sign-up', methods=['post', 'get'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if db.session.query(Gamer).filter(Gamer.login == login).first() is None:
            gamer = Gamer()
            gamer.name = name
            gamer.login = login
            gamer.password_hash = generate_password_hash(password)
            db.session.add(gamer)
            db.session.commit()

            response = make_response(redirect('/personal_area'))
            response.set_cookie('gamer_id', str(gamer.id), max_age=None)
            return response
        else:
            return render_template('/sign_up.html', message="пользователем с таким логином уже существует")
    else:
        return render_template('/sign_up.html')


@app.route('/personal_area')
def show_personal_area():
    gamer_id = int(request.cookies.get('gamer_id'))
    gamer = db.session.query(Gamer).filter(Gamer.id == gamer_id).first()
    success_levels = db.session.query(Level).join(Session, Session.id == Level.session_id).join(Gamer,
    Session.gamer_id == gamer_id).filter(Level.success == 1).order_by(Level.level_num).all()

    if success_levels:
        level_num = success_levels[-1].level_num
    else:
        level_num = 0

    session = Session()
    session.gamer_id = gamer_id
    db.session.add(session)
    db.session.commit()

    response = make_response(render_template('/personal_area.html', name=gamer.name.title(), level_num=level_num))
    response.set_cookie('session_id', str(session.id), max_age=None)
    return response


@app.route('/personal_area/statistics')
def show_statistics():
    gamer_id = int(request.cookies.get('gamer_id'))
    levels = db.session.query(Level).join(Session, Session.id == Level.session_id).join(Gamer,
    Session.gamer_id == gamer_id).all()

    count = len(levels)
    level_nums = [level.level_num for level in levels]

    numbers = [[] for _ in range(count)]
    answers = [[] for _ in range(count)]

    for i in range(count):
        numbers_list = db.session.query(NumbersList).filter(NumbersList.level_id == levels[i].id).first()
        answers_list = db.session.query(AnswersList).filter(AnswersList.level_id == levels[i].id).first()

        if (length := levels[i].numbers_count) > 0:
            numbers[i].append(numbers_list.n1)
            if answers_list is not None:
                answers[i].append(answers_list.n1)
        if length > 1:
            numbers[i].append(numbers_list.n2)
            if answers_list is not None:
                answers[i].append(answers_list.n2)
        if length > 2:
            numbers[i].append(numbers_list.n3)
            if answers_list is not None:
                answers[i].append(answers_list.n3)
        if length > 3:
            numbers[i].append(numbers_list.n4)
            if answers_list is not None:
                answers[i].append(answers_list.n4)
        if length > 4:
            numbers[i].append(numbers_list.n5)
            if answers_list is not None:
                answers[i].append(answers_list.n5)
        if length > 5:
            numbers[i].append(numbers_list.n6)
            if answers_list is not None:
                answers[i].append(answers_list.n6)
        if length > 6:
            numbers[i].append(numbers_list.n7)
            if answers_list is not None:
                answers[i].append(answers_list.n7)
        if length > 7:
            numbers[i].append(numbers_list.n8)
            if answers_list is not None:
                answers[i].append(answers_list.n8)

    numbers = [', '.join(map(str, numbers[i])) for i in range(len(answers))]
    answers = [', '.join(map(str, answers[i])) for i in range(len(answers))]

    successes = ['пройден' if level.success == 1 else 'провален' for level in levels]

    return render_template('/statistics.html', count=count, level_nums=level_nums, numbers=numbers, answers=answers,
                           successes=successes)


@app.route('/game')
def show_game_level():
    session_id = int(request.cookies.get('session_id'))
    levels_list = db.session.query(Level).filter(Level.session_id == session_id).all()

    level = Level()
    level.level_num = len(levels_list) + 1

    if level.level_num <= 7:
        level.minimum, level.maximum = 0, 9
        level.numbers_count = level.level_num + 1
    elif level.level_num <= 14:
        level.minimum, level.maximum = 10, 99
        level.numbers_count = level.level_num - 6
    else:
        level.minimum, level.maximum = 100, 999
        level.numbers_count = level.level_num - 13

    level.digits_count = len(str(level.minimum))
    level.session_id = session_id
    db.session.add(level)
    db.session.commit()

    numbers_list = NumbersList()
    numbers = [randint(level.minimum, level.maximum) for _ in range(level.numbers_count)]

    numbers_list.n1 = numbers[0]
    numbers_list.n2 = numbers[1]

    if (length := len(numbers)) > 2:
        numbers_list.n3 = numbers[2]
    if length > 3:
        numbers_list.n4 = numbers[3]
    if length > 4:
        numbers_list.n5 = numbers[4]
    if length > 5:
        numbers_list.n6 = numbers[5]
    if length > 6:
        numbers_list.n7 = numbers[6]
    if length > 7:
        numbers_list.n8 = numbers[7]

    numbers_list.level_id = level.id
    db.session.add(numbers_list)
    db.session.commit()

    return render_template('show_numbers.html', level=level.level_num, numbers=numbers)


@app.route('/answers', methods=['post', 'get'])
def get_user_answers():
    session_id = int(request.cookies.get('session_id'))
    level = db.session.query(Level).filter(Level.session_id == session_id).all()[-1]

    if request.method == 'POST':
        answers_list = AnswersList()

        answers_list.n1 = request.form.get('n1')
        answers_list.n2 = request.form.get('n2')

        if (length := level.numbers_count) > 2:
            answers_list.n3 = request.form.get('n3')
        if length > 3:
            answers_list.n4 = request.form.get('n4')
        if length > 4:
            answers_list.n5 = request.form.get('n5')
        if length > 5:
            answers_list.n6 = request.form.get('n6')
        if length > 6:
            answers_list.n7 = request.form.get('n7')
        if length:
            answers_list.n8 = request.form.get('n8')

        answers_list.level_id = level.id
        db.session.add(answers_list)
        db.session.commit()

        return redirect('/results')

    return render_template('answers.html', level=level.level_num, numbers_count=level.numbers_count,
                           digits_count=level.digits_count, minimum=level.minimum, maximum=level.maximum)


@app.route('/results')
def show_results():
    session_id = int(request.cookies.get('session_id'))
    gamer_id = int(request.cookies.get('gamer_id'))
    gamer = db.session.query(Gamer).filter(Gamer.id == gamer_id).first()
    level = db.session.query(Level).filter(Level.session_id == session_id).all()[-1]
    numbers_list = db.session.query(NumbersList).filter(NumbersList.level_id == level.id).first()
    answers_list = db.session.query(AnswersList).filter(AnswersList.level_id == level.id).first()

    if numbers_list.n1 == answers_list.n1 and numbers_list.n2 == answers_list.n2 \
            and numbers_list.n3 == answers_list.n3 and numbers_list.n4 == answers_list.n4 \
            and numbers_list.n5 == answers_list.n5 and numbers_list.n6 == answers_list.n6 \
            and numbers_list.n7 == answers_list.n7 and numbers_list.n8 == answers_list.n8:
        level.success = 1
        db.session.add(level)
        db.session.commit()

        if level.level_num != 21:
            check = 1
            return render_template('results.html', check=check, name=gamer.name)
        else:
            check = 2
            return render_template('results.html', check=check, name=gamer.name)

    else:
        check = 3
        numbers = [numbers_list.n1, numbers_list.n2]

        if (length := level.numbers_count) > 2:
            numbers.append(numbers_list.n3)
        if length > 3:
            numbers.append(numbers_list.n4)
        if length > 4:
            numbers.append(numbers_list.n5)
        if length > 5:
            numbers.append(numbers_list.n6)
        if length > 6:
            numbers.append(numbers_list.n7)
        if length > 7:
            numbers.append(numbers_list.n8)

        return render_template('results.html', check=check, name=gamer.name, numbers=', '.join(map(str, numbers)))
