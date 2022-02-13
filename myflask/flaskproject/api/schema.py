from marshmallow import fields
from api.models import Post,Car
from api.config import ma

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content")
        model = Post

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

class CarSchema(ma.Schema):
    class Meta:
        fields=('id','sub_modelid','price')
        model=Car

car_schema=CarSchema()
cars_schema=CarSchema(many=True)
