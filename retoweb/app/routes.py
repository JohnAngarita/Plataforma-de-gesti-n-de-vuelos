from flask import render_template, flash, redirect, url_for, request
from flask_wtf import form
from app import app
from app.forms import LoginForm, RegistroForm, ComenForm, Crearvuelo

from flask_login import current_user, login_user
from app.models import *
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

from app import db
from app.forms import RegistroForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('serviciousuario')
        return redirect(next_page)
    return render_template('login.html',  title='Inicio sesion', titulo='Inicio de sesión Usuario registrado', form=form)

@app.route('/registrousuario', methods=['GET', 'POST'])
def registrousuario():
    if current_user.is_authenticated:
        return redirect(url_for('index'))    
    form = RegistroForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, nombre=form.nombre.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Gracias por registrarse {}'.format(form.username.data))
        return redirect(url_for('login'))
    return render_template('registrousuario.html',title='Register', titulo='Registro Usuarios', form=form)

@app.route('/serviciousuario')
@login_required
def serviciousuario():
    return render_template('serviciousuario.html')

@app.route('/calificarvuelo', methods=['GET', 'POST'])
@login_required
def califvuelo():
    form = ComenForm()
    if request.method == 'POST' and form.validate():
        flash('Gracias por sus comentarios')
        return redirect(url_for('calificarvuelo'))
    return render_template('calificarvuelo.html', title='Usuario', titulo='Calificación y comentarios', form=form)
    
@app.route('/calificarvuelo')
@login_required
def calificarvuelo():
    return render_template('calificarvuelo.html', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
    
@app.route('/loginpiloto', methods=['GET', 'POST'])
def loginpiloto():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Pilot.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('loginpiloto'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('serviciopiloto')
        return redirect(next_page)
    return render_template('loginpiloto.html',  title='Inicio sesion', form=form)
    
 
@app.route('/serviciopiloto')
@login_required
def serviciopiloto():
    return render_template('serviciopilto.html')
    
    
    
@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('loginadmin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('servicioadmin')
        return redirect(next_page)
    return render_template('loginadmin.html',  title='Inicio sesion', form=form)
    
@app.route('/registroadmin', methods=['GET', 'POST'])
def registroadmin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))    
    form = RegistroForm()
    if form.validate_on_submit():
        user = Admin(username=form.username.data, nombre=form.nombre.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Gracias por registrarse {}'.format(form.username.data))
        return redirect(url_for('loginadmin'))
    return render_template('registroadmin.html',title='Register', form=form)
    
@app.route('/servicioadmin')
@login_required
def servicioadmin():
    return render_template('servicioadmin.html', title='Admin', titulo='Servicios Administrador')

@app.route('/registropiloto', methods=['GET', 'POST'])
@login_required
def registropiloto():
    
    form = RegistroForm()
    if form.validate_on_submit():
        user = Pilot(username=form.username.data, nombre=form.nombre.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Gracias por registrarse {}'.format(form.username.data))
        return redirect(url_for('loginpiloto'))
    return render_template('registropiloto.html',title='Register', titulo='Registro Pilotos', form=form)
    
@app.route('/crearvuelo', methods=['GET', 'POST'])
@login_required
def crearvuelo():
    
    form = Crearvuelo()
    flash('Codigo del vuelo:  %s %s' % (form.origen.data, form.matricula.data))
  
    if form.validate_on_submit():
        vuelo = Vuelo(codigo=form.codigo.data, fecha=form.fecha.data, hora=form.hora.data, destino=form.destino.data, origen=form.origen.data, matricula=form.matricula.data, aerolineas=form.aerolineas.data, capacidades=form.capacidades.data, piloto=form.piloto.data, estados=form.estados.data )
        db.session.add(vuelo)
        db.session.commit()
        flash('Vuelo creado {}'.format(form.codigo.data))
        return redirect(url_for('servicioadmin'))
    return render_template('crearvuelo.html',  title='Sesion Admin', titulo='Servicios Administrador', form=form)
    
