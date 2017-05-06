from .shared import db


class User(db.Model):

    __tablename__ = 'getin_user'

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

        # TODO remove test code ----------------
        if name == 'Celeo Servasse':
            self.editor = True
            self.admin = True

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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fits = db.relationship('Fit', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Fit(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.String)

    def __init__(self, name, category_id, content=''):
        self.name = name
        self.category_id = category_id
        self.content = content
