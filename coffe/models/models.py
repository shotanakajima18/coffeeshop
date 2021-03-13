from coffe.database import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship



class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    screen_name = db.Column(db.String(21), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(80))
    tel=db.Column(db.String(11))
    admin=db.Column(db.Boolean, default=False)
    
    
    perchase_drink = db.relationship("Perchase_drink", back_populates = 'users')
    perchase_food = db.relationship("Perchase_food", back_populates = 'users')

    def __init__(self, screen_name, email, password, tel):
        self.screen_name = screen_name
        self.email = email
        self.tel=tel
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.screen_name)

class Drink(UserMixin, db.Model):
    __tablename__ = 'drink'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    
    flavar = db.Column(db.String(20))
    price =db.Column(db.Integer)
    picture = db.Column(db.String(20))

    perchase_drink = db.relationship("Perchase_drink", back_populates = 'drink')

    def __init__(self, flavar, price, picture):
        
        
        self.flavar=flavar
        self.price=price
        self.picture=picture

    def __repr__(self):
        return '<Drink %r>' %(self.flavar)


class Foods(UserMixin, db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name =  db.Column(db.String(20))
    quantity =db.Column(db.Integer)
    price =db.Column(db.Integer)
    picture =db.Column(db.String(20))

    perchase_food = db.relationship("Perchase_food", back_populates = 'food')

    def __init__(self, quantity, name, price, picture):
        self.quantity = quantity
        self.name= name
        self. price=price
        self.picture=picture
    def __repr__(self):
        return '<Foods %r>' %(self.name)

class Perchase_drink(UserMixin,db.Model):
    __tablename__='perchase_drink'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'))

    size=db.Column(db.Integer)
    tem=db.Column(db.String(10))
    quantity =db.Column(db.Integer)
    price =db.Column(db.Integer)
    
    

    def __init__(self,user_id,tem, drink_id,price,quantity ,size):
        self.user_id= user_id
        self.drink_id=drink_id

        self.size=size
        self.tem=tem
        self.price=price
        self.quantity = quantity
        
        
    def __repr__(self):
        return '<perchase_drink %r>' %(self.name)

    users = db.relationship("User", back_populates = 'perchase_drink')
    drink= db.relationship("Drink", back_populates = 'perchase_drink')

class Perchase_food(UserMixin, db.Model):
    __tablename__='perchase_food'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))

    quantity =db.Column(db.Integer)
    price =db.Column(db.Integer)

    def __init__(self,user_id, food_id, price,quantity):
        self.quantity = quantity
        self.user_id=user_id
        self.food_id=food_id
        self. price=price
        

    def __repr__(self):
        return '<perchase_food %r>' %(self.name)

    users = db.relationship("User", back_populates = 'perchase_food')
    food= db.relationship("Foods", back_populates = 'perchase_food')

    



    
    

