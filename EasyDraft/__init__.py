from flask import Flask
from database.database import Database
from EasyDraft.config import BaseConfig, PROJECT
from flask.ext.login import LoginManager
from flask_oauth import OAuth

app = Flask(PROJECT)
app.config.from_object(BaseConfig)
login_manager = LoginManager()
login_manager.setup_app(app)
database = Database(app)
oauth = OAuth()
yahoo = oauth.remote_app('yahoo',
        base_url='http://fantasysports.yahooapis.com/fantasy/v2/',
        request_token_url='https://api.login.yahoo.com/oauth/v2/get_request_token',
        access_token_url='https://api.login.yahoo.com/oauth/v2/get_token',
        authorize_url='https://api.login.yahoo.com/oauth/v2/request_auth',
        consumer_key='dj0yJmk9SlBOaEx5VjJvRjJMJmQ9WVdrOWIyOVZiMUZpTnpnbWNHbzlNVE0xTURnNE1UVTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD1hOA--',
        consumer_secret='eb800ec46583d123c8df54ac2c28f5d2975c06d9'
        )

import EasyDraft.views
