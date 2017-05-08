from flask_restful import fields

from .shared import db


class User(db.Model):

    __tablename__ = 'getin_user'

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'corporation': fields.String,
        'alliance': fields.String,
        'editor': fields.Boolean,
        'admin': fields.Boolean,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    corporation = db.Column(db.String)
    alliance = db.Column(db.String)
    editor = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, name, corporation, alliance, editor=False, admin=False):
        self.name = name
        self.corporation = corporation
        self.alliance = alliance
        self.editor = editor
        self.admin = admin

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def in_alliance(self):
        return self.alliance == 'The Society For Unethical Treatment Of Sleepers'

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return '<User-{}>'.format(self.name)


class Category(db.Model):

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'order': fields.Integer,
        'has_linked_fits': fields.Boolean
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    order = db.Column(db.Integer)
    fits = db.relationship('Fit', backref='category', lazy='dynamic')

    def __init__(self, name, order=100):
        self.name = name
        self.order = order

    @property
    def has_linked_fits(self):
        return self.fits.count() > 0


class Fit(db.Model):

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'category_id': fields.Integer,
        'content': fields.String,
        'order': fields.Integer,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.String)
    order = db.Column(db.Integer)

    def __init__(self, name, category_id=None, content='', order=100):
        self.name = name
        self.category_id = category_id or Category.query.first().id
        self.content = content
        self.order = order
