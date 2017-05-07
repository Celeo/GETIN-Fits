from flask_restful import Resource

from ..util import authenticate
from ..models import Category, Fit, db


class CategoriesResource(Resource):

    method_decorators = [authenticate]

    def get(self):
        categories = sorted(Category.query.all(), key=lambda x: x.name)

        # TODO remove test code
        if not categories:
            self.load_test_data()
            categories = sorted(Category.query.all(), key=lambda x: x.name)

        data = [{
            'name': category.name,
            'ships': [
                {
                    'name': fit.name,
                    'fit': fit.content
                } for fit in category.fits
            ]} for category in categories]
        return data

    def load_test_data(self):
        db.session.add(Category('PVE'))
        db.session.add(Category('PVP'))
        db.session.add(Fit('Scorpion', 1, '# test data here'))
        db.session.commit()
