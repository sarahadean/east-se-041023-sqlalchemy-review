from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

#~~~~~Note~~~~~__repr__ is how class will show in Flask shell

# create model Car, License, Color
# create tablenames - plural of class
# relationship vs association proxy?
#association_proxy('relationship to intermediary', 'relationship from intermediary to target')

class Car(db.Model):
    __tablename__ = 'cars'
    
    # create id, created_at, and updated_at columns
    # create column company
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String)
    
    # create relationship to license and color: 
    license_plates = db.relationship('License', back_populates='car')

    #both arguments of association_proxy are relationships
    colors_of_cur_car = association_proxy('license_plates','color',)

    def __repr__(self):
        return f'<Car hello manufacturer={self.manufacturer} id={self.id}/>'


# create model colors
class Color(db.Model):
    # create tablename colors
    __tablename__ = 'colors'
    
    # create id, created_at, and updated_at columns
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # create column color
    color = db.Column(db.String)
    
    # create relationship to license
    license_plates = db.relationship('License', back_populates='color')
    # create relationship to car
    cars_with_cur_color = association_proxy('license_plates', 'car')

# create model license
class License(db.Model):
    # create tablename licenses
    __tablename__ = 'licenses'
    # create id, created_at, and updated_at columns
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #create column license_plate
    license_plate = db.Column(db.String)
    # create foreign keys to color, car
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    # create relationship to color, car
    car = db.relationship('Car', back_populates='license_plates')
    color = db.relationship('Color', back_populates='license_plates')


