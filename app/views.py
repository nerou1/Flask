from flask.views import MethodView
from flask import jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import generate_password_hash, check_password_hash
from app.models import Users, Ads
from datetime import datetime

auth = HTTPBasicAuth()


class UsersView(MethodView):

    def get(self, user_id=None):
        if user_id is not None:
            user = Users.query.get(user_id)
            if not user:
                response = jsonify(
                    {
                        'error': 'User not found'
                    }
                )
                response.status_code = 404
                return response
            return jsonify(
                {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            )
        else:
            users = []
            for user in Users.query.all():
                users.append(
                    {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email
                    }
                )
            return jsonify({'users': users})

    def post(self):
        user = Users(**request.json)
        user.password = generate_password_hash(user.password)
        try:
            user.add()
            return jsonify(
                {
                    'status': 'created',
                    'id': user.id
                }
            )
        except Exception as e:
            return jsonify(
                {
                    'error': e.args[0]
                }
            )


class AdsView(MethodView):

    @auth.login_required
    def post(self):
        ad = Ads(**request.json)
        email = request.authorization.username
        ad.user_id = Users.query.filter_by(email=email).first().id
        ad.adv_date = datetime.now()
        try:
            ad.add()
            return jsonify(
                {
                    'status': 'created',
                    'id': ad.id
                }
            )
        except Exception as e:
            return jsonify(
                {
                    'error': e.args[0]
                }
            )

    @auth.login_required
    def delete(self, ad_id):
        email = request.authorization.username
        user_id = Users.query.filter_by(email=email).first().id
        ad = Ads.query.filter_by(id=ad_id).first()
        if ad.user_id == user_id:
            Ads.query.filter_by(id=ad_id).delete()
            ad.commit()
            return jsonify(
                {
                    'status': 'removed',
                    'ad_id': ad_id
                }
            )
        else:
            response = jsonify(
                {
                    'error': 'Unauthorized',
                    'ad_id': ad_id
                }
            )
            response.status_code = 401
            return response

    @auth.login_required
    def patch(self, ad_id):
        email = request.authorization.username
        user_id = Users.query.filter_by(email=email).first().id
        ad = Ads.query.filter_by(id=ad_id).first()
        ad.title = request.json.get('title')
        ad.description = request.json.get('description')
        if ad.user_id == user_id:
            ad.commit()
            return jsonify(
                {
                    'id': ad_id,
                    'title': ad.title,
                    'description': ad.description
                }
            )
        else:
            response = jsonify(
                {
                    'error': 'Unauthorized',
                    'ad_id': ad_id
                }
            )
            response.status_code = 401
            return response

    def get(self):
        ads = []
        for ad in Ads.query.all():
            ads.append(
                {
                    'id': ad.id,
                    'title': ad.title,
                    'description': ad.description,
                    'adv_date': ad.adv_date,
                    'user_id': ad.user_id
                }
            )
        return jsonify({'ads': ads})

    @staticmethod
    @auth.verify_password
    def verify_password(username, password):
        user = Users.query.filter_by(email=username).first()
        if not user or not check_password_hash(user.password, password):
            return False
        return True