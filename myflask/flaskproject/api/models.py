from enum import unique

from sqlalchemy.orm import backref
from api.config import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titles = db.Column(db.String(50))
    content = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.title
    
    
class Emp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titles = db.Column(db.String(50))
    content = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.title


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id=db.Column(db.String,unique=True)
    email=db.Column(db.String)
    password=db.Column(db.String)
    first_name=db.Column(db.String(50))
    last_name=db.Column(db.String(50))


class Car(db.Model):
    id=db.Column(db.String,primary_key=True)
    active=db.Column(db.String)
    year=db.Column(db.String)
    mileage=db.Column(db.String)
    price=db.Column(db.String)
    make_id=db.Column(db.String)
    model_id=db.Column(db.String)
    sub_modelid=db.Column(db.String)
    body_type=db.Column(db.String)
    transmission=db.Column(db.String)
    fuel_type=db.Column(db.String)
    exterior_color=db.Column(db.String)
    created_at=db.Column(db.String)
    updated_at=db.Column(db.String)
   
    

class CarMakes(db.Model):
    __tablename__='carmakes'
    id=db.Column(db.String(50),primary_key=True,autoincrement=False)
    # unique_id=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(50))
    active=db.Column(db.String)
    created_at=db.Column(db.String(255))
    updated_at=db.Column(db.String(255))
    carmakes=db.relationship('CarModels',backref='carmakes',lazy=True)
    
    

class CarModels(db.Model):
    __tablename__='carmodels'
    id=db.Column(db.String(50),primary_key=True,autoincrement=False)
    # unique_id=db.Column(db.Integer,unique=True)
    name=db.Column(db.String(50))
    active=db.Column(db.String)
    make_id=db.Column(db.String(50))
    created_at=db.Column(db.String(255))
    updated_at=db.Column(db.String(255))
    carmakes_id=db.Column(db.String,db.ForeignKey('carmakes.id'),nullable=False)
    carsubmodles=db.relationship('CarSubModels',backref='carmodels',lazy=True)
 

class CarSubModels(db.Model):
    __tablename__='carsubmodels'
    id=db.Column(db.String(50),primary_key=True,autoincrement=False)
    # unique_id=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(50))
    active=db.Column(db.String)
    model_id=db.Column(db.String)
    created_at=db.Column(db.String(255))
    updated_at=db.Column(db.String(255))
    car_model_id=db.Column(db.String,db.ForeignKey('carmodels.id'),nullable=False)




