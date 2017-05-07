from flask import request
from flask_restful import Resource

from ..util import authenticate
from ..models import db, Fit, Category


class FitsResource(Resource):

    method_decorators = [authenticate]

    def get(self):
        fit_list = [
            {
                'id': fit.id,
                'name': fit.name,
                'category': fit.category.name,
                'category_id': fit.category.id,
                'content': fit.content
            } for fit in Fit.query.all()
        ]
        category_list = [
            {
                'id': category.id,
                'name': category.name
            } for category in Category.query.all()
        ]
        return {
            'fits': sorted(fit_list, key=lambda e: e.order),
            'categories': sorted(category_list, key=lambda e: e.order)
        }

    def post(self):
        db.session.add(Fit(request.json['name']))
        db.session.commit()
        return {}, 204

    def put(self):
        # TODO need more authentication on this endpoint as well
        # TODO implement
        return {}, 204


class FitResource(Resource):

    # TODO need to futher restrict access to
    #   these 2 endpoints based on permissions
    method_decorators = [authenticate]

    def put(self, id):
        fit = Fit.query.get(id)
        fit.content = request.json['content']
        fit.category_id = request.json['category_id']
        db.session.commit()
        return {}, 204

    def delete(self, id):
        db.session.delete(Fit.query.get(id))
        db.session.commit()
        return {}, 204
