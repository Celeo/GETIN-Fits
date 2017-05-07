from flask import request
from flask_restful import Resource

from ..util import authenticate
from ..models import db, Fit


class FitsResource(Resource):

    method_decorators = [authenticate]

    def get(self):
        fits = Fit.query.all()
        data = [
            {
                'id': fit.id,
                'name': fit.name,
                'category': fit.category.name,
                'content': fit.content
            } for fit in fits]
        return data


class FitResource(Resource):

    method_decorators = [authenticate]

    def put(self, id):
        Fit.query.get(id).content = request.json['content']
        db.session.commit()
        return {}, 204
