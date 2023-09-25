from flask import Flask
from app.config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from app import models, views
from app.models import db

API_ROOT = '/api/v1/'
app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

app.add_url_rule(API_ROOT + 'users/', view_func=views.UsersView.as_view('users_get'), methods=['GET',], defaults={'user_id': None})
app.add_url_rule(API_ROOT + 'users/<int:user_id>', view_func=views.UsersView.as_view('user_get'), methods=['GET',])
app.add_url_rule(API_ROOT + 'users/', view_func=views.UsersView.as_view('users_post'), methods=['POST',])

app.add_url_rule(API_ROOT + 'ads/', view_func=views.AdsView.as_view('ads_get'), methods=['GET',])
app.add_url_rule(API_ROOT + 'ads/', view_func=views.AdsView.as_view('ads_post'), methods=['POST',])
app.add_url_rule(API_ROOT + 'ads/<int:ad_id>', view_func=views.AdsView.as_view('ads_patch'), methods=['PATCH',])
app.add_url_rule(API_ROOT + 'ads/<int:ad_id>', view_func=views.AdsView.as_view('ads_delete'), methods=['DELETE',])



if __name__ == 'main':
    app.run()