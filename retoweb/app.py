from flask import Flask, render_template, request, flash, redirect, url_for

import yagmail as yagmail
import os

app=Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/loginUsuario")
def loginUsuario():
    return render_template("loginUsuario.html")

@app.route("/registroUsuario")
def registroUsuario():
    return render_template("registroUsuario.html")

@app.route("/loginPilotos")
def loginPilotos():
    return render_template("loginPilotos.html")

@app.route("/loginAdmin")
def loginAdmin():
    return render_template("loginAdmin.html")

@app.route("/reservaVuelos")
def reservaVuelos():
    return render_template("reservaVuelos.html")
    reservaVuelos

@app.route("/registroVuelo")
def registroVuelo():
    return render_template("registroVuelo.html")

@app.route("/editVuelo")
def editVuelo():
    return render_template("editVuelo.html")

@app.route("/busquedaVuelo")
def busquedaVuelo():
    return render_template("busquedaVuelo.html")

@app.route("/eliminarVuelo")
def eliminarVuelo():
    return render_template("eliminarVuelo.html")

@app.route("/vuelosRealizado")
def vuelosRealizado():
    return render_template("vuelosRealizado.html")

@app.route("/loginUsuarioRes")
def loginUsuarioRes():
    return render_template("loginUsuarioRes.html")

@app.route("/verUsuarios")
def verUsuarios():
    return render_template("verUsuarios.html")

@app.route("/eliminarUsuario")
def eliminarUsuario():
    return render_template("eliminarUsuario.html")

@app.route("/editarUsuario")
def editarUsuario():
    return render_template("editarUsuario.html")

@app.route("/calificarVuelo")
def calificarVuelo():
    return render_template("calificarVuelo.html")

@app.route("/verComentarios")
def verComentarios():
    return render_template("verComentarios.html")




    
 
   
