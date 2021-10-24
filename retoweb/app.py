from datetime import date, datetime
import re
from sqlite3 import dbapi2
from flask import Flask
from flask import render_template, request, redirect

from db import get_db

app=Flask(__name__)

@app.route("/")
def index():
   return render_template ("index.html")

@app.route("/index")
def inicio():
   return render_template ("index.html")

@app.route("/inicio")
def inicios():
   return render_template ("inicio.html")

@app.route("/verVuelos")
def verVuelos():
    db = get_db()
    sql = """SELECT vuelo.id,
            id_ciudad_origen,
            origen.ciudad,
            id_ciudad_destino,
            destino.ciudad,
            fecha,
            hora,
            id_avion,
            avion.avion,
            vuelo.id_aerolinea,
            aerolinea.aerolinea,
            id_piloto,
            piloto.nombre,
            estado,
            estado_vuelo.nombre_est
        FROM vuelo
        INNER JOIN avion ON avion.id = id_avion
        INNER JOIN aerolinea ON aerolinea.id = vuelo.id_aerolinea
        INNER JOIN piloto ON piloto.id = id_piloto
        INNER JOIN ciudad as origen ON origen.id = id_ciudad_origen
        INNER JOIN ciudad as destino ON destino.id = id_ciudad_destino
        INNER JOIN estado_vuelo as estado_vuelo ON estado_vuelo.id = vuelo.estado"""

    vuelos = db.execute(sql).fetchall()
    return render_template('verVuelos.html', vuelos = vuelos)

#Usuarios
@app.route("/createUser")
def createUser():
    return render_template("createUser.html")

@app.route("/addUser", methods=["POST"])
def addUser():
    db = get_db()
    nombre = request.form['nomUsuario']
    usuario = request.form['userUsuario']
    sexo = request.form['sexoUsuario']
    correo = request.form['emailUsuario']
    cod_rol = request.form['rolUsuario']
    contrasena = request.form['contUsuario']
    sql = "INSERT INTO usuario (nombre,usuario,sexo,correo,contrasena,cod_rol) VALUES ('{}','{}','{}','{}','{}','{}')".format(nombre, usuario, sexo, correo, contrasena, '1')
        
    db.execute(sql)
    db.commit()
    return redirect("/verUser")

@app.route("/loginUsuario")
def loginUsuario():
    return render_template("loginUsuario.html")

@app.route("/logUsuario", methods=["GET", "POST"])
def logUsuario():
    if request.method =="POST":
        user = request.form['userUsuario']
        password = request.form['contUsuario']
        sql = "SELECT * FROM usuario WHERE usuario = '" + user + "' and contrasena = '" + password + "' and cod_rol = '1'"
        db = get_db()
        usuarios = db.execute(sql).fetchall()
        if usuarios:
            vuelos = db.execute(
                """SELECT vuelo_realizado.id,
                        id_vuelo,
                        vuelo.fecha,
                        vuelo.hora,
                        ciudad.ciudad as CiudadOrigen,
                        c2.ciudad as CiudadDes,
                        id_usuario
                    FROM vuelo_realizado
                    INNER JOIN vuelo on vuelo.id = vuelo_realizado.id_vuelo
                    INNER JOIN ciudad ON ciudad.id = vuelo.id_ciudad_origen
                    INNER JOIN ciudad as c2 ON c2.id = vuelo.id_ciudad_destino"""
            ).fetchall()
            return render_template('verVueloRealizado.html', vuelos = vuelos)
        else:
            return render_template('loginUsuario.html')
    else:
        return render_template('loginUsuario.html')

#Usuario Administrador
@app.route("/verUser")
def verUser():
    db = get_db()
    usuarios = db.execute(
        'SELECT usuario.id, usuario.Nombre, usuario.Usuario, usuario.sexo, usuario.Correo, usuario.contrasena, rol.nombre_rol FROM usuario INNER JOIN rol ON rol.id = usuario.cod_rol'
    ).fetchall()
    return render_template('verUser.html', usuarios = usuarios)

@app.route("/delUser/<int:id>")
def eliminar(id):
    sql = 'DELETE FROM usuario where id=' + str(id)
    db = get_db()
    db.execute(sql)
    db.commit()
    return redirect("/verUser")

@app.route("/addUsuario")
def addUsuario():
    return render_template("addUsuario.html")

@app.route("/addUsers", methods=["POST"])
def addUsers():
    db = get_db()
    nombre = request.form['nomUsuario']
    usuario = request.form['userUsuario']
    sexo = request.form['sexoUsuario']
    correo = request.form['emailUsuario']
    cod_rol = request.form['rolUsuario']
    contrasena = request.form['contUsuario']
    sql = "INSERT INTO usuario (nombre,usuario,sexo,correo,contrasena,cod_rol) VALUES ('{}','{}','{}','{}','{}','{}')".format(nombre, usuario, sexo, correo, contrasena, cod_rol)
        
    db.execute(sql)
    db.commit()
    return redirect("/verUser")

@app.route("/editUser/<int:id>")
def edituser(id):
    sql = 'SELECT * FROM usuario WHERE ID = ' +str(id)
    db = get_db()
    usuarios = db.execute(sql).fetchall()
    return render_template('edituser.html', usuarios = usuarios)

@app.route("/updateUser", methods=["POST"])
def update():
    db = get_db()
    id = request.form['idVuelo']
    aerolinea = request.form['vueloAerolinea']
    origen = request.form['vueloOrigen']
    destino = request.form['vueloDestino']
    fecha = request.form['vueloFecha']
    hora = request.form['vueloHora']
    piloto = request.form['vueloPiloto']
    avion = request.form['vueloAvion']
    
    sql = "UPDATE usuario SET id_aerolinea = '" + str(aerolinea) + "', id_ciudad_origen = '" + str(origen) + "', id_ciudad_destino = '" + str(destino) + "', fecha = '" + fecha + "', hora = '" + hora + "', id_piloto = '" + str(piloto) + "', id_avion = '" + str(avion) + "' WHERE id = " + str(id) 
    print(sql)    
    db.execute(sql)
    db.commit()
    return redirect("/verUser")

@app.route("/loginAdministrador")
def loginAdministrador():
    return render_template("loginAdministrador.html")

@app.route("/logUsuarioAdm", methods=["GET", "POST"])
def logUsuarioAdm():
    if request.method =="POST":
        user = request.form['userUsuario']
        password = request.form['contUsuario']
        sql = "SELECT * FROM usuario WHERE usuario = '" + user + "' and contrasena = '" + password + "' and cod_rol = '3'"
        db = get_db()
        usuarios = db.execute(sql).fetchall()
        if usuarios:
            return render_template('inicio.html')
        else:
            return render_template('loginAdministrador.html')
    else:
        return render_template('logUsuarioAdm.html')

#Vuelos
@app.route("/verVuelo")
def verVuelo():
    db = get_db()
    sql = """SELECT vuelo.id,
            id_ciudad_origen,
            origen.ciudad,
            id_ciudad_destino,
            destino.ciudad,
            fecha,
            hora,
            id_avion,
            avion.avion,
            vuelo.id_aerolinea,
            aerolinea.aerolinea,
            id_piloto,
            piloto.nombre,
            estado,
            estado_vuelo.nombre_est
        FROM vuelo
        INNER JOIN avion ON avion.id = id_avion
        INNER JOIN aerolinea ON aerolinea.id = vuelo.id_aerolinea
        INNER JOIN piloto ON piloto.id = id_piloto
        INNER JOIN ciudad as origen ON origen.id = id_ciudad_origen
        INNER JOIN ciudad as destino ON destino.id = id_ciudad_destino
        INNER JOIN estado_vuelo as estado_vuelo ON estado_vuelo.id = vuelo.estado""" 

    vuelos = db.execute(sql).fetchall()
    return render_template('verVuelo.html', vuelos = vuelos)

@app.route("/createVuelo")
def createVuelo():
    db = get_db()
    ciudad = db.execute('SELECT * FROM ciudad').fetchall()
    aerolinea = db.execute('SELECT * FROM aerolinea').fetchall()
    avion = db.execute('SELECT * from avion').fetchall()
    piloto = db.execute('SELECT * from piloto').fetchall()
    return render_template("createVuelo.html", aerolinea = aerolinea, avion = avion, ciudad = ciudad, piloto = piloto)

@app.route("/delVuelo/<int:id>")
def delVuelo(id):
    sql = 'DELETE FROM vuelo where id=' + str(id)
    db = get_db()
    db.execute(sql)
    db.commit()
    return redirect("/verVuelo")

@app.route("/updateVuelo", methods=["POST"])
def updateVuelo():
    db = get_db()
    id = request.form['idVuelo']
    aerolinea = request.form['vueloAerolinea']
    origen = request.form['vueloOrigen']
    destino = request.form['vueloDestino']
    fecha = request.form['vueloFecha']
    hora = request.form['vueloHora']
    piloto = request.form['vueloPiloto']
    avion = request.form['vueloAvion']
    estado = request.form['vueloEstado']
    sql = "UPDATE vuelo SET id_aerolinea = '" + str(aerolinea) + "', id_ciudad_origen = '" + str(origen) + "', id_ciudad_destino = '" + str(destino) + "', fecha = '" + fecha + "', hora = '" + hora + "', id_piloto = '" + str(piloto) + "', id_avion = '" + str(avion) + "', estado = '" + str(estado) + "' WHERE id = " + str(id) 
    print(sql)    
    db.execute(sql)
    db.commit()
    return redirect("/verVuelo")

@app.route("/editVuelo/<int:id>")
def editVuelo(id):
    db = get_db()
    sql = 'SELECT * FROM vuelo WHERE ID = ' +str(id)
    ciudad = db.execute('SELECT * FROM ciudad').fetchall()
    aerolinea = db.execute('SELECT * FROM aerolinea').fetchall()
    avion = db.execute('SELECT * from avion').fetchall()
    piloto = db.execute('SELECT * from piloto').fetchall()
    estado = db.execute('SELECT * from estado_vuelo').fetchall()
    vuelos = db.execute(sql).fetchall()
    return render_template("editVuelo.html", aerolinea = aerolinea, avion = avion, ciudad = ciudad, piloto = piloto, vuelos = vuelos, estado = estado)

@app.route("/addVuelo", methods=["POST"])
def addVuelo():
    db = get_db()
    aerolinea = request.form['vueloAerolinea']
    origen = request.form['vueloOrigen']
    destino = request.form['vueloDestino']
    fecha = request.form['vueloFecha']
    hora = request.form['vueloHora']
    piloto = request.form['vueloPiloto']
    avion = request.form['vueloAvion']
    sql = "INSERT INTO vuelo (id_aerolinea,id_ciudad_origen,id_ciudad_destino,fecha,hora,id_piloto,id_avion,estado) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(aerolinea, origen, destino, fecha, hora, piloto, avion, "1")
        
    db.execute(sql)
    db.commit()
    return redirect("/verVuelo")

#Aviones
@app.route("/verAvion")
def verAvion():
    db = get_db()
    aviones = db.execute('SELECT * from avion').fetchall()
    return render_template('verAvion.html', aviones = aviones)

@app.route("/createAvion")
def createAvion():
    return render_template("createAvion.html")

@app.route("/addAvion", methods=["POST"])
def addAvion():
    db = get_db()
    nombre = request.form['nomAvion']
    capacidad = request.form['avionCapacidad']
    sql = "INSERT INTO avion (avion,capacidad) VALUES ('{}','{}')".format(nombre, capacidad)  
    db.execute(sql)
    db.commit()
    return redirect("/verAvion")

@app.route("/updateAvion", methods=["POST"])
def updateAvion():
    db = get_db()
    id = request.form['idAvion']
    avion = request.form['nomAvion']
    capacidad = request.form['capAvion']
    sql = "UPDATE avion SET avion = '" + avion + "', capacidad = '" + capacidad + "' WHERE id = " + str(id) 
    print(sql)    
    db.execute(sql)
    db.commit()
    return redirect("/verAvion")

@app.route("/delAvion/<int:id>")
def delAvion(id):
    sql = 'DELETE FROM avion where id=' + str(id)
    db = get_db()
    db.execute(sql)
    db.commit()
    return redirect("/verAvion")

@app.route("/editAvion/<int:id>")
def editAvion(id):
    sql = 'SELECT * FROM avion WHERE ID = ' +str(id)
    db = get_db()
    aviones = db.execute(sql).fetchall()
    return render_template('editAvion.html', aviones = aviones)

#Aerolinea
@app.route("/verAerolinea")
def verAerolinea():
    db = get_db()
    aerolineas = db.execute('SELECT * from aerolinea').fetchall()
    return render_template('verAerolinea.html', aerolineas = aerolineas)

@app.route("/createAerolinea")
def createAerolinea():
    return render_template("createAerolinea.html")

@app.route("/addAerolinea", methods=["POST"])
def addAerolinea():
    db = get_db()
    nombre = request.form['nomAerolinea']
    sql = "INSERT INTO aerolinea (aerolinea) VALUES ('{}')".format(nombre)  
    db.execute(sql)
    db.commit()
    return redirect("/verAerolinea")

@app.route("/updateAerolinea", methods=["POST"])
def updateAerolinea():
    db = get_db()
    id = request.form['idAerolinea']
    aerolinea = request.form['nomAerolinea']
    sql = "UPDATE aerolinea SET aerolinea = '" + aerolinea + "' WHERE id = " + str(id) 
    print(sql)    
    db.execute(sql)
    db.commit()
    return redirect("/verAerolinea")

@app.route("/delAerolinea/<int:id>")
def delAerolinea(id):
    sql = 'DELETE FROM aerolinea where id=' + str(id)
    db = get_db()
    db.execute(sql)
    db.commit()
    return redirect("/verAerolinea")

@app.route("/editAerolinea/<int:id>")
def editAerolinea(id):
    sql = 'SELECT * FROM aerolinea WHERE ID = ' +str(id)
    db = get_db()
    aerolineas = db.execute(sql).fetchall()
    return render_template('editAerolinea.html', aerolineas = aerolineas)

#Ciudad
@app.route("/verCiudad")
def verCiudad():
    db = get_db()
    ciudades = db.execute('SELECT * from Ciudad').fetchall()
    return render_template('verCiudad.html', ciudades = ciudades)

@app.route("/createCiudad")
def createCiudad():
    return render_template("createCiudad.html")

@app.route("/addCiudad", methods=["POST"])
def addCiudad():
    db = get_db()
    nombre = request.form['nomCiudad']
    sql = "INSERT INTO Ciudad (ciudad) VALUES ('{}')".format(nombre)  
    db.execute(sql)
    db.commit()
    return redirect("/verCiudad")

@app.route("/updateCiudad", methods=["POST"])
def updateCiudad():
    db = get_db()
    id = request.form['idCiudad']
    Ciudad = request.form['nomCiudad']
    sql = "UPDATE Ciudad SET ciudad = '" + Ciudad + "' WHERE id = " + str(id) 
    print(sql)    
    db.execute(sql)
    db.commit()
    return redirect("/verCiudad")

@app.route("/delCiudad/<int:id>")
def delCiudad(id):
    sql = 'DELETE FROM Ciudad where id=' + str(id)
    db = get_db()
    db.execute(sql)
    db.commit()
    return redirect("/verCiudad")

@app.route("/editCiudad/<int:id>")
def editCiudad(id):
    sql = 'SELECT * FROM Ciudad WHERE ID = ' +str(id)
    db = get_db()
    ciudades = db.execute(sql).fetchall()
    return render_template('editCiudad.html', ciudades = ciudades)

#Estado
@app.route("/verEstado")
def verEstado():
    db = get_db()
    estados = db.execute('SELECT * from estado_vuelo').fetchall()
    return render_template('verEstado.html', estados = estados)

@app.route("/createEstado")
def createEstado():
    return render_template("createEstado.html")

@app.route("/addEstado", methods=["POST"])
def addEstado():
    db = get_db()
    nombre = request.form['nomEstado']
    sql = "INSERT INTO estado_vuelo (nombre_est) VALUES ('{}')".format(nombre)  
    db.execute(sql)
    db.commit()
    return redirect("/verEstado")

@app.route("/updateEstado", methods=["POST"])
def updateEstado():
    db = get_db()
    id = request.form['idEstado']
    Estado = request.form['nomEstado']
    sql = "UPDATE estado_vuelo SET nombre_est= '" + Estado + "' WHERE id = " + str(id) 
    print(sql)    
    db.execute(sql)
    db.commit()
    return redirect("/verEstado")

@app.route("/delEstado/<int:id>")
def delEstado(id):
    sql = 'DELETE FROM estado_vuelo where id=' + str(id)
    db = get_db()
    db.execute(sql)
    db.commit()
    return redirect("/verEstado")

@app.route("/editEstado/<int:id>")
def editEstado(id):
    sql = 'SELECT * FROM estado_vuelo WHERE ID = ' +str(id)
    db = get_db()
    estados = db.execute(sql).fetchall()
    return render_template('editEstado.html', estados = estados)

#Pilotos
@app.route("/verPiloto")
def verPiloto():
    db = get_db()
    pilotos = db.execute('SELECT * from Piloto').fetchall()
    return render_template('verPiloto.html', pilotos = pilotos)

@app.route("/createPiloto")
def createPiloto():
    return render_template("createPiloto.html")

@app.route("/addPiloto", methods=["POST"])
def addPiloto():
    db = get_db()
    piloto = request.form['nomPiloto']
    experiencia = request.form['expPiloto']
    sql = "INSERT INTO Piloto (nombre,experiencia) VALUES ('{}','{}')".format(piloto, experiencia)  
    db.execute(sql)
    db.commit()
    return redirect("/verPiloto")

@app.route("/updatePiloto", methods=["POST"])
def updatePiloto():
    db = get_db()
    id = request.form['idPiloto']
    piloto = request.form['nomPiloto']
    experiencia = request.form['expPiloto']
    sql = "UPDATE Piloto SET nombre = '" + piloto + "', experiencia = '" + experiencia + "' WHERE id = " + str(id) 
    print(sql)    
    db.execute(sql)
    db.commit()
    return redirect("/verPiloto")

@app.route("/delPiloto/<int:id>")
def delPiloto(id):
    sql = 'DELETE FROM Piloto where id=' + str(id)
    db = get_db()
    db.execute(sql)
    db.commit()
    return redirect("/verPiloto")

@app.route("/editPiloto/<int:id>")
def editPiloto(id):
    sql = 'SELECT * FROM Piloto WHERE ID = ' +str(id)
    db = get_db()
    pilotos = db.execute(sql).fetchall()
    return render_template('editPiloto.html', pilotos = pilotos)

@app.route("/verVueloRealizado")
def verVueloRealizado():
    db = get_db()
    vuelos = db.execute(
                """SELECT vuelo_realizado.id,
                        id_vuelo,
                        vuelo.fecha,
                        vuelo.hora,
                        ciudad.ciudad as CiudadOrigen,
                        c2.ciudad as CiudadDes,
                        id_usuario
                    FROM vuelo_realizado
                    INNER JOIN vuelo on vuelo.id = vuelo_realizado.id_vuelo
                    INNER JOIN ciudad ON ciudad.id = vuelo.id_ciudad_origen
                    INNER JOIN ciudad as c2 ON c2.id = vuelo.id_ciudad_destino"""
    ).fetchall()
    return render_template('verVueloRealizado.html', vuelos = vuelos)
    
@app.route("/reservaVuelo")
def reservaVuelo():
    return render_template("reservaVuelo.html")

@app.route("/Vuelos")
def Vuelos():
    db = get_db()
    sql = """SELECT vuelo.id,
            id_ciudad_origen,
            origen.ciudad,
            id_ciudad_destino,
            destino.ciudad,
            fecha,
            hora,
            id_avion,
            avion.avion,
            vuelo.id_aerolinea,
            aerolinea.aerolinea,
            id_piloto,
            piloto.nombre,
            estado,
            estado_vuelo.nombre_est
        FROM vuelo
        INNER JOIN avion ON avion.id = id_avion
        INNER JOIN aerolinea ON aerolinea.id = vuelo.id_aerolinea
        INNER JOIN piloto ON piloto.id = id_piloto
        INNER JOIN ciudad as origen ON origen.id = id_ciudad_origen
        INNER JOIN ciudad as destino ON destino.id = id_ciudad_destino
        INNER JOIN estado_vuelo as estado_vuelo ON estado_vuelo.id = vuelo.estado"""

    vuelos = db.execute(sql).fetchall()
    return render_template('Vuelos.html', vuelos = vuelos)

@app.route("/createComentario/<int:idVuelo>/<int:idUser>")
def createComentario(idVuelo,idUser):
    sql = 'SELECT * FROM usuario WHERE ID = ' +str(idUser)
    db = get_db()
    usuarios = db.execute(sql).fetchall()
    sql = 'SELECT * FROM vuelo WHERE ID = ' +str(idVuelo)
    vuelos = db.execute(sql).fetchall()
    return render_template("createComentario.html", usuarios = usuarios, vuelos = vuelos)

@app.route('/createCalificacion/<int:idVuelo>/<int:idUser>')
def createCalificacion(idVuelo,idUser):
    sql = 'SELECT * FROM usuario WHERE ID = ' +str(idUser)
    db = get_db()
    usuarios = db.execute(sql).fetchall()
    sql = 'SELECT * FROM vuelo WHERE ID = ' +str(idVuelo)
    vuelos = db.execute(sql).fetchall()
    return render_template("createCalificacion.html", usuarios = usuarios, vuelos = vuelos)

@app.route("/addNota", methods=["POST"])
def addNota():
    db = get_db()
    codUser = request.form['usua']
    fly = request.form['nomVuelo']
    cal = request.form['vueloCalificacion']
    sql = "INSERT INTO calificacion (nota,id_vuelo,id_usuario) VALUES ('{}','{}','{}')".format(cal,fly,codUser)  
    db.execute(sql)
    db.commit()
    return redirect("/verVueloRealizado")

@app.route("/addComentario", methods=["POST"])
def addComentario():
    
    codUser = request.form["idUser"]
    fly = request.form['idVuelo']
    com = request.form['vueloComentario']
    sql = "INSERT INTO comentario (comentario,id_vuelo,id_usuario) VALUES ('{}','{}','{}')".format(com,fly,codUser)  
    db = get_db()
    db.execute(sql)
    db.commit()
    return redirect("/verVueloRealizado")

if __name__ == '__main__':
    app.run(debug=True)
