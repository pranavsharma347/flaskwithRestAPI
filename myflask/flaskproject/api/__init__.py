from api.views import PostListResource,PostResource,UserLogin, UserLogut, UserRegister,docs,CarData
from flask_restful import Api, Resource
from api.views import flaskAppInstance,api,csv
from flask_migrate import Migrate


# csv()

api=Api(flaskAppInstance)


api.add_resource(PostListResource, '/post')
docs.register(PostListResource)
api.add_resource(PostResource, '/posts/<int:post_id>')
docs.register(PostResource)
api.add_resource(UserRegister,'/userregister')
docs.register(UserRegister)
api.add_resource(UserLogin,'/userlogin/<string:email>/<string:password>/')
docs.register(UserLogin)
api.add_resource(UserLogut,'/logout')
docs.register(UserLogut)
api.add_resource(CarData,'/cardata/<string:start_price>/<string:end_price>/')
# docs.register(CarData)
    


# api.add_resource(UploadImage,'/fileupload/<string:file>')
# docs.register(UploadImage)