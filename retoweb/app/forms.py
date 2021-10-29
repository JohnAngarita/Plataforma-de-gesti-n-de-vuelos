from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import User, Pilot, Admin
from wtforms.fields import DateTimeField
from app import consultas
import sqlite3

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(message=('Ingrese un dato valido'))])
    password = PasswordField('Contraseña', validators=[DataRequired(message=('Ingrese un dato valido'))])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Enviar')

class RegistroForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message=('Ingrese un dato valido')), Length(min=4, max=15, message=('Ingrese un dato valido minimo 4 y máximo 15 caracteres'))])
    email = EmailField('Correo electronico', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre y apellido', validators=[DataRequired(message=('Ingrese un dato valido'))])
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('confirm', message='Las contraseñas deben coincidir'), Length(min=8, max=12, message=('Ingrese una contraseña de minimo 8 y máximo 12 caracteres')) ])
    confirm = PasswordField('Repita Contraseña')
    accept_tos = BooleanField('Apecto terminos y condiciones', validators=[DataRequired(message=('Acepte confirmación'))])
    submit = SubmitField('Enviar')

class ComenForm(FlaskForm):
    busquevuelo = StringField('Seleccion Vuelo', validators=[DataRequired(message=('Ingrese un dato valido'))], render_kw={"placeholder": "Buscar Vuelo"})
    comentario = TextAreaField('Escribe tu Comentario', validators=[DataRequired(message=('Ingrese un dato valido'))], render_kw={"placeholder": "Escribe tu comentario"})
    submit = SubmitField('Enviar')
    
class Crearvuelo(FlaskForm):
        
    codigo = StringField('Codigo: ', validators=[DataRequired(message=('Ingrese un dato valido'))], render_kw={"placeholder": "Codigo Vuelo"})
    fecha = StringField('Fecha: ', validators=[DataRequired(message=('Ingrese una fecha valida'))], render_kw={"placeholder": "Fecha Vuelo"})
    hora = StringField('Hora: ', validators=[DataRequired(message=('Ingrese una hora valida'))], render_kw={"placeholder": "Hora Vuelo"})
    #destino = StringField('Destino: ', validators=[DataRequired(message=('Ingrese un dato valido'))], render_kw={"placeholder": "Destino"})
    destino = SelectField(u'Destino', choices = [('LETICIA'), ('ARMENIA'), ('BUCARAMANGA'), ('BOGOTA'), ('BARRANQUILLA'), ('CUCUTA'), ('CARTAGENA'), ('CALI'), ('TUMACO'), ('COROZAL'), ('BARRANCABERMEJA'), ('FLORENCIA'), ('CARTAGO'), ('GUAPI'), ('GUAYMARAL'), ('IBAGUE'), ('IPIALES'), ('CAREPA')], validators = [DataRequired()])
    
    #origen = StringField('Origen: ', validators=[DataRequired(message=('Ingrese un dato valido'))], render_kw={"placeholder": "Origen"})
    origen = SelectField(u'Origen', choices = [('LETICIA'), ('ARMENIA'), ('BUCARAMANGA'), ('BOGOTA'), ('BARRANQUILLA'), ('CUCUTA'), ('CARTAGENA'), ('CALI'), ('TUMACO'), ('COROZAL'), ('BARRANCABERMEJA'), ('FLORENCIA'), ('CARTAGO'), ('GUAPI'), ('GUAYMARAL'), ('IBAGUE'), ('IPIALES'), ('CAREPA')], validators = [DataRequired()])
    
    matricula = StringField('Matricula: ', validators=[DataRequired(message=('Ingrese un dato valido'))], render_kw={"placeholder": "Matricula"})
    aerolineas = StringField('Aerolinea: ', validators=[DataRequired(message=('Ingrese un dato valido'))], render_kw={"placeholder": "Aerolinea"})
    capacidades = StringField('Capacidad: ', validators=[DataRequired(message=('Ingrese un dato valido'))], render_kw={"placeholder": "Capacidad"})
    piloto = StringField('Piloto: ', validators=[DataRequired(message=('Ingrese un dato valido'))], render_kw={"placeholder": "Piloto"})
    estados = SelectField(u'Estados', choices = [('A tiempo'), ('Retrazado'), ('Aterrizo'), ('Despego')], validators = [DataRequired()])
    
    submit = SubmitField('Crear: ')   


    
      