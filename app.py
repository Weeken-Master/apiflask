
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

from .actions.chart1_action import Chart1Action
from .models.chart1_model import Chart1
from .models.user_model import User
from .actions.user_action import UserAction
from .Model_crawl import TongQuanThiTruong
from .Model_crawl import DanhMuc
# from .models import chart1_model
# from .models import user_model

from .models.market_analytics_model import market_analytics
from .actions.market_analytics_action import market_analytics_action


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
connection_data=pymysql.connect(host="localhost", user="root", passwd="", db="flyseo_db") 
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
        'message': 'Hello World',
        'status': 'Success'
    }
    return jsonify(result)



# @app.route('/index', methods=['POST'])
# def index():
#     return 'Index page'

# Get all customer
# @app.route('/chart1')
# # xài jwt phân quyền đăng nhập mới cho xem hoặc admin ms có quyền xem   
# @jwt_required()
# def homes():
#     chart1_action = Chart1Action(connection_data)
#     result = chart1_action.get_all()
#     return jsonify(result)


# # Get all customer
# @app.route('/chart12')
# # xài jwt c admin ms có quyền xem   
# @jwt_required()
# def homes2():
#     # lấy thông tin token hiện tại
#     current_user = get_jwt_identity();
#     if(current_user['role']=='Admin'):
#         chart1_action = Chart1Action(connection_data)
#         result = chart1_action.get_all()
#         return jsonify(result)
  
#     return "Bạn không phải admin"
@app.route('/chart1/<int:id>', methods =['GET','PUT','POST','DELETE'])
def get_or_modify_chart1(id):
    if(request.method =='GET'):
        #get id
        chart1action = Chart1Action(connection_data)
        result, StatusCode = chart1action.get_by_id(id)
        if(StatusCode == 200):
            return jsonify({
                'data':result}), StatusCode
        #400
        return jsonify({'Message':result}),StatusCode

    elif(request.method == 'DELETE'):
        chart_id = Chart1(ID=id)
        print("ha",chart_id)
        chart1action = Chart1Action(connection_data)
        messgae,StatusCode = chart1action.delete(chart_id)
        return jsonify({'Message':messgae}),StatusCode
        #chỉnh sửa
    elif(request.method =='PUT'):
       # json
        #body = request.json # dictionary

        #customer_name = body.get('customer_name', '')
        #contact_name = body.get('contact_name', '')
        Product = request.form['Product'] 
        Price = request.form ['Price']
        chart1= Chart1(Product=Product, Price= Price  )
        chart1_action = Chart1Action(connection_data)
        message, status_code = chart1_action.update(id, chart1)
        return jsonify({
            'message': message
        }), status_code
    else:
        # 405
        pass
    return "Message: Not Found"
@app.route('/chart1', methods=['POST'])
def add_chart1():
    # Get data from request body
    Product = request.form['Product'] 
    Price = request.form ['Price']
    chart1= Chart1(Product=Product, Price = Price)
    chart1_action = Chart1Action(connection_data)
    message ="",StatusCode;
    try:
        message, status_code = chart1_action.add(chart1)
    except:
        ""
    return  message,status_code

@app.route('/api/v4/getdata1',methods=['GET'])
def getdata1():
    chart1_action = Chart1Action(connection_data)
    result = chart1_action.get_all()
    return jsonify(result)






#  viết api chính thức
@app.route('/apiv4/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username)
    if  username == None or password is None:
        return jsonify({
            'message': 'Missing username or password'
        }), 400
    data_login = User(username=username, password=password)
    user_action = UserAction(connection_data)
    result, status_code = user_action.login(data_login)
   
    if status_code != 200:
        return jsonify({
            'message': result
        }), status_code
    # 200 Luu thong tin user vao token
    access_token = create_access_token(identity=result.serialize())

    return jsonify({
        'token': access_token
    })
@app.route('/apiv4/authorizon/decode_token', methods =['GET'])
def decodelogin():
    # datatoken  =  request.form['token']
    # print(datatoken)
    # if not datatoken:
    #     return jsonify({'message': 'a valid token is missing'})
    if request.endpoint != '/decode_token':
        verify_jwt_in_request();
        
    current_user= get_jwt_identity();
    return jsonify(login=current_user), 200



@app.route('/apiv4/register', methods =['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    print(username)
    if username == None or password is None:
        return jsonify({
            'message': 'Missing username or password'
        }), 400
    data_register = User(username=username,password=password)
    user_action = UserAction(connection_data)
    result, status_code = user_action.register(data_register)
    if(status_code == 200):
        return jsonify({
            'message': result
        }), status_code
 
    return jsonify


# API TỔNG QUAN VỀ THỊ TRƯỜNG
@app.route('/apiv4/model/tongquanthitruong', methods =['GET'])
def datatongquan():
    data = TongQuanThiTruong.getdatamarket();
    if(data == None):
         return  'Fail model', 400
    return data

@app.route('/apiv4/chart/tongquanthitruong', methods=["GET"])
def chartTT():
    datas = TongQuanThiTruong.getdatachartmaket();
    if( datas == None):
        return 'Fail model',400
    return datas



# update phân tích thị trường về phần danh mục bán chạy pho bien, moi nhat 
# @app.route('/apiv4/marketanalytics/match_id=',methods=["POST"])
# def market_analytics_model():
#     match_id = request.form['match_id'];
#     data = DanhMuc.crawlalldanhmuc(match_id);
#     return data,200

# get data phân tích thị trường mới nhất 
@app.route('/apiv4/get_data_market/match_id=', methods =['POST'])
def get_or_modify_data_market():
    try:
        match_id = request.form['match_id'];
        if(request.method =='POST' ):
            #get match_id
            Market_analytics_action = market_analytics_action(connection_data)
            result, StatusCode = Market_analytics_action.get_by_match_id(match_id)
            if(StatusCode == 200):
                return jsonify({
                    'datas':result}), StatusCode
            #400
            return jsonify({'Message':result}),StatusCode
    except:
        return 'Fail',401



# update  dữ liệu  danh mục giành cho admin + add vào sql
@app.route('/apiv4/admin/update/marketanalytics/match_id=', methods=["POST"])
def market_analytics_admin():
    match_id = request.form['match_id'];
   
    print("TK FONTEND NÓ GỬI LÊN", match_id)
    data = DanhMuc.crawlalldanhmuc(match_id);
    
    if(data != None):
        #print("aaaaaaaaaaaaaaaaaaa",data["MoiNhat"])
        selling = data["BanChay"];
        newest = data["MoiNhat"];
        popular = data["PhoBien"];
        timeupdate = data["timeupdate"];

        print("-----------------")
 
        Market_analytics_data= market_analytics(match_id=match_id, selling = selling , newest = newest, popular = popular, timeupdate= timeupdate )
        Market_analytics_action = market_analytics_action(connection_data)
        message ="",StatusCode;
        try:
            message, status_code = Market_analytics_action.add(Market_analytics_data)
        except:
             ""
        return  message,status_code
    return data,200

if __name__ == '__main__':
    app.run(port=5000,host="0.0.0.0",debug=True)