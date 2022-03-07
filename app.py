
# from crypt import methods
from tokenize import Token
from flask import Flask
from flask import jsonify
from flask import request
from flask.typing import StatusCode
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import JWTManager
from sqlalchemy.sql.functions import char_length, current_user
from flask_cors import CORS



import pymysql
import ast
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.debug = True
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})
# mã hóa
# này dung de mã hóa cái thông tin sau mã hóa dc mã token 
app.config['JWT_SECRET_KEY'] = 'FlySeo'
jwt = JWTManager(app)

"""
METHOD:
    1. GET
    2. POST
    3. PUT(PATCH)
    4. DELETE
"""
def parse_str(s):
   try:
      return ast.literal_eval(str(s))
   except:
      return
@app.route('/', methods=['GET', 'POST'])
def home():
    result = {
        'message': 'Hello World TUẦN ĐÂY',
        'status': 'Success'
    }
    return jsonify(result)




if __name__ == '__main__':
    app.run(port=5000,host="0.0.0.0",debug=True)
