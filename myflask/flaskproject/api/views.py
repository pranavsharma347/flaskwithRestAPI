from enum import unique
from flask_apispec.views import MethodResource
import jwt
from marshmallow import Schema, fields
import uuid
from flask_apispec import use_kwargs
from api.config import db
from api.models import Post,Register,CarMakes,CarModels,CarSubModels,Car
from api.schema import post_schema,cars_schema
from flask_restful import Api, Resource
from flask import Flask, app ,request
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_cors import CORS
from app import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import datetime
from flask import Flask, jsonify, request, session
from datetime import datetime,timedelta
from jwt import PyJWT
from functools import wraps
from flask.views import View
import werkzeug
from flask_restful import reqparse
import pandas as pd
import os



 
api=Api(flaskAppInstance)

flaskAppInstance.config['SECRET_KEY'] = '7503d534b05a4b288fa9e577a07ab35c'

flaskAppInstance.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)

# flaskAppInstance.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(flaskAppInstance)

flaskAppInstance.config.update({
    'APISPEC_SPEC': APISpec(
        title='Flask Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/'  # URI to access UI of API Doc
})

docs=FlaskApiSpec(flaskAppInstance)

def token_required(f):
    @wraps(f)
    def decorated(current_user,*args,**kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        if not token:
            return jsonify({'message':'token is missing'})
        try:
            data=jwt.decode(token,flaskAppInstance.config['SECRET_KEY'],algorithms=["HS256"])
            current_user=Register.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message':'token is invalid'})
        return f(current_user,*args,**kwargs)
    return decorated



class PostListResource(MethodResource,Resource):
    @token_required
    def get(self):
        posts = Post.query.all()
        return post_schema.dump(posts,many=True)
    
    @token_required
    @use_kwargs({'title':fields.Str(),'content':fields.Str()})
    def post(self,**kwargs):        
        new_post = Post(
        titles=request.json['title'],
        content=request.json['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)
            
 
# api.add_resource(PostListResource, '/post')
# docs.register(PostListResource)


class PostResource(MethodResource,Resource):
    @token_required
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)
    
    @token_required
    @use_kwargs({'titles':fields.Str(),'content':fields.Str()})
    def patch(self, post_id,**kwargs):
        post = Post.query.get_or_404(post_id)

        if 'titles' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return post_schema.dump(post)
       
       
    @token_required
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        
# api.add_resource(PostResource, '/posts/<int:post_id>')
# docs.register(PostResource)
       
       



class UserRegister(MethodResource,Resource):
    @use_kwargs({'email':fields.Str(),'password':fields.Str(),'first_name':fields.Str(),'last_name':fields.Str()})
    def post(self):
        user=Register.query.filter_by(email=request.json['email']).first()
        if user:
            return jsonify({'message' : 'please choose a unique email'})
        else:
            password=generate_password_hash(request.json['password'])#sconvert password in hash format
            user_register=Register(email=request.json['email'],
            public_id=str(uuid.uuid4()),
            password=password,first_name=request.json['first_name'],
            last_name=request.json['last_name'])
            db.session.add(user_register)
            db.session.commit()
            return "user registered successfully"
        
        
# api.add_resource(UserRegister,'/userregister')
# docs.register(UserRegister)

class UserLogin(MethodResource,Resource):
    def get(self,email,password):
            user=Register.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password,password):
                    token=jwt.encode({'public_id':user.public_id,
                    'exp':datetime.utcnow() + timedelta(minutes = 15)},
                    flaskAppInstance.config['SECRET_KEY'])

                    return jsonify({'token':token.decode('UTF-8')})
                else:
                    return "invalid password"
            else:
                return 'invalid user'

# api.add_resource(UserLogin,'/userlogin/<string:email>/<string:password>/')
# docs.register(UserLogin)

class UserLogut(MethodResource,Resource):
    @token_required
    def get(self,**kwargs):
            return jsonify({'message' : 'You successfully logged out'})
        
# api.add_resource(UserLogut,'/logout')
# docs.register(UserLogut)

#now userlogin using session

# class UserLogin(Resource):
#     def get(self,email,password):
#         user=Register.query.filter_by(email=email).first()
#         if user:
#             if check_password_hash(user.password,password):
#                 session['email']=request.json['email']
#                 return jsonify({"user login successfully":session['email']})
#             else:
#                 return "invalid password"
#         else:
#             return "invalid user"

# class UserLogut(Resource):
#     def get(self):
        
#         if 'email' in session:
#             session.pop('email', None)
#             return jsonify({'message' : 'You successfully logged out'})
         

from werkzeug.utils import secure_filename
import os

 

def csv():
    path=os.getcwd()
    directory=f"{path}/file/"
    for filename in sorted(os.listdir(directory)):
        print(filename)
        f = os.path.join(directory, filename)
        df=pd.read_csv(f,sep=',',error_bad_lines=False, index_col=False,warn_bad_lines=False,dtype='unicode')

        for index,row in df.iterrows():
            if filename=='makes1.csv':
                # if os.path.isfile(f"{f}"):
                #     print(filename,'is already available')
                #     break
                # else:
                if CarMakes.query.filter_by(id=row['id']).first():
                    pass
                else:    
                    carmakes=CarMakes(id=row['id'],name=row['name'],active=row['active'],created_at=row['created_at'],
                    updated_at=row['updated_at'])
                    db.session.add(carmakes)
                    db.session.commit()

            elif filename=='models.csv':
                data=CarMakes.query.filter_by(id=row['make_id']).first()
                if data.id==row['make_id']:
                    # if os.path.isfile(f"{f}"):
                    #     print(filename,'is already available')
                    #     break
                    # else:
                    if CarModels.query.filter_by(id=row['id']).first():
                        pass

                    else:
                        carmodels=CarModels(id=row['id'],name=row['name'],active=row['active'],make_id=row['make_id'],created_at=row['created_at'],
                        updated_at=row['updated_at'],carmakes_id=data.id)
                        db.session.add(carmodels)
                        db.session.commit()

            elif filename=='submodels.csv':
                data=CarModels.query.filter_by(id=row['model_id']).first()
                if data.id==row['model_id']:
                    if CarSubModels.query.filter_by(id=row['id']).first():
                        pass
                    else:
                        carsubmodels=CarSubModels(id=row['id'],name=row['name'],active=row['active'],model_id=row['model_id'],created_at=row['created_at'],
                        updated_at=row['updated_at'],car_model_id=data.id)
                        db.session.add(carsubmodels)
                        db.session.commit()

            # elif filename=='car.csv':
            #     if Car.query.filter_by(id=row['id']).first():
            #         pass
            #     else:
            #         car=Car(id=row['id'],active=row['active'],year=row['year'],mileage=row['mileage'],price=row['price'],
            #         make_id=row['make_id'],model_id=row['model_id'],sub_modelid=row['submodel_id'],body_type=row['body_type'],
            #         transmission=row['transmission'],fuel_type=row['fuel_type'], exterior_color=row['exterior_color'],
            #         created_at=row['created_at'],updated_at=row['updated_at'])
            #         db.session.add(car)
            #         db.session.commit()
            
class CarData(Resource):

    def get(self,start_price,end_price):
        data=Car.query.filter(Car.price>=start_price).filter(Car.price<=end_price)
        print(data.count())
        # .filter(Car.mileage>start_mileage).filter(Car.mileage<end_mileage)
        return cars_schema.dump(data)



                
            # elif filename=='submodels.csv':
            #     print('working')
            #     carsubmodels=CarSubModels(id=row['id'],name=row['name'],active=row['active'],model_id=row['model_id'],
            #     created_at=row['created_at'],updated_at=row['updated_at'])
            #     db.session.add(carsubmodels)
            #     db.session.commit()
        

    # df1=pd.read_csv(f"{path}/file/cars.csv",sep=',', error_bad_lines=False, index_col=False, dtype='unicode',warn_bad_lines=False)
    # print('cars',df1)
    # df2=pd.read_csv(f"{path}/file/makes.csv",sep=',', error_bad_lines=False, index_col=False, dtype='unicode',warn_bad_lines=False)
    # print('makes',df2)
    # df3=pd.read_csv(f"{path}/file/models.csv",sep=',', error_bad_lines=False, index_col=False, dtype='unicode',warn_bad_lines=False)
    # print('models',df3)
    # df4=pd.read_csv(f"{path}/file/submodels.csv",sep=',', error_bad_lines=False, index_col=False, dtype='unicode',warn_bad_lines=False)
    # print('submodels',df4)

    # for index,row in df.iterrows():
    #     if os.path.isfile(f"{path}/file/6.csv"):
    #         print('file is already available')
    #         break
    #     else:
    #         print('email',row['email'])
    #         data=Register(email=row['email'],password=row['password'],first_name=row['first_name'],last_name=row['last_name'])
    #         db.session.add(data)
    #         db.session.commit()        
    

    




