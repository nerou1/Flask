from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class SaveMixin():
    def add(self):
        db.session.add(self)
        db.session.commit()

    def commit(self):
        db.session.commit()


class Users(db.Model, SaveMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), index=True, unique=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(64), nullable=False)
    ads = db.relationship('Ads', backref='owner', lazy='dynamic')


class Ads(db.Model, SaveMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True, unique=True)
    description = db.Column(db.String(255))
    adv_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))