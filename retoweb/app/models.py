from app import db
'''Linea nueva para genenerar el has del password'''
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from sqlalchemy.orm import *



class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(244), index=True, unique=True)
    nombre = db.Column(db.String(244))
    email = db.Column(db.String(244), unique=True)
    password_hash = db.Column(db.String(244))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    '''Linea nueva para genenerar el has del password'''
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
        
class Pilot(UserMixin, db.Model):
    __tablename__ = "pilot"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(244), unique=True)
    nombre = db.Column(db.String(244))
    email = db.Column(db.String(244), unique=True)
    password_hash = db.Column(db.String(244))
     
    def __repr__(self):
        return '<Pilot {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Admin(UserMixin, db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(244), unique=True)
    nombre = db.Column(db.String(244))
    email = db.Column(db.String(244), index=True, unique=True)
    password_hash = db.Column(db.String(244))

    def __repr__(self):
        return '<Admin {}>'.format(self.username)
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
        
class Plane(db.Model):
    __tablename__ = "plane"
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(244), unique=True)
    aerolinea = db.Column(db.String(244))
    capacidad = db.Column(db.Integer)
      
    def __repr__(self):
        return '<Plane {}>'.format(self.matricula, self.aerolinea, self.capacidad)
        
class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True)
    cityname = db.Column(db.String(244), nullable = False)
    codename = db.Column(db.String(244), unique=True)
    pais = db.Column(db.String(244))
    type = db.Column(db.String(244))
   

    def __repr__(self):
        return '<City {}>'.format(self.cityname, self.codename)

class Estado(db.Model):
    __tablename__ = "estado"
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(244))

    def __repr__(self):
        return '<Estado {}>'.format(self.estado)
        
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(244))
    

    def __repr__(self):
        return '<Comment {}>'.format(self.comment)
        
class Vuelo(db.Model):
    __tablename__ = "vuelo"
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(244))
    fecha = db.Column(db.String, index=True, nullable = False)
    hora = db.Column(db.String, index=True, nullable = False)
    destino = db.Column(db.String(244))
    origen = db.Column(db.String(244))
    matricula = db.Column(db.String(244))
    aerolineas = db.Column(db.String(244))
    capacidades = db.Column(db.String(244))
    piloto = db.Column(db.String(244))
    estados = db.Column(db.String(244))

    def __repr__(self):
        return '<Vuelo {}>'.format(self.vuelo, self.origen, self.destino, self.fecha, self.hora, self.matricula, self.capacidad, self.aerolinea, self.piloto, self,estado)
       
       
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

'''@login.pilot_loader
def load_pilot(id):
    return Pilot.query.get(int(id))
    
    
@login.admin_loader
def load_admin(id):
    return Admin.query.get(int(id))'''
    