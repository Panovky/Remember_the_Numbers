from app import db


class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    gamer_id = db.Column(db.Integer, db.ForeignKey('gamer.id'), nullable=False)


class Gamer(db.Model):
    __tablename__ = 'gamer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    login = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)


class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True)
    level_num = db.Column(db.Integer, nullable=False)
    digits_count = db.Column(db.Integer, nullable=False)
    numbers_count = db.Column(db.Integer, nullable=False)
    minimum = db.Column(db.Integer, nullable=False)
    maximum = db.Column(db.Integer, nullable=False)
    success = db.Column(db.Integer, default=0)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)


class NumbersList(db.Model):
    __tablename__ = 'numbers'
    id = db.Column(db.Integer, primary_key=True)
    n1 = db.Column(db.Integer, nullable=False)
    n2 = db.Column(db.Integer, nullable=False)
    n3 = db.Column(db.Integer)
    n4 = db.Column(db.Integer)
    n5 = db.Column(db.Integer)
    n6 = db.Column(db.Integer)
    n7 = db.Column(db.Integer)
    n8 = db.Column(db.Integer)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)


class AnswersList(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    n1 = db.Column(db.Integer, nullable=False)
    n2 = db.Column(db.Integer, nullable=False)
    n3 = db.Column(db.Integer)
    n4 = db.Column(db.Integer)
    n5 = db.Column(db.Integer)
    n6 = db.Column(db.Integer)
    n7 = db.Column(db.Integer)
    n8 = db.Column(db.Integer)
    minutes = db.Column(db.Integer, nullable=False)
    seconds = db.Column(db.Integer, nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
