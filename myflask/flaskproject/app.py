from flask_sqlalchemy import SQLAlchemy # new
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask import Flask ,request






flaskAppInstance = Flask(__name__)
 # new

if __name__ == '__main__':
    from api import *
    flaskAppInstance.run(host='127.0.0.1',port=8000, debug=True, use_reloader=True)
