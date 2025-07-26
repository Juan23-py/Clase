from flask import Flask, jsonify,request
from flask_cors import CORS
import pymysql                    #en caso de no funcionar la libreria se utiliza lda libreria " pymysql"msyql-connector-python
import pymysql.cursors            #para llamar el cursor o formato diccionario se agrega este archivo 

app= Flask(__name__)
CORS(app)
listaPersonas = []

db = pymysql.connect(
    host="localhost",
    user="root",           
    password="Juan12345.",     
    database="sabadoJulio" 
)
cursor = db.cursor(pymysql.cursors.DictCursor)  #para la otra libreria se utiliza  "dictionary=true"     

@app.route("/mensaje",methods=["GET"])
def mensaje():
    return "Primera aplicacion wed"

@app.route("/listarPersonas",methods=["GET"])
def listar():
    return jsonify(listaPersonas) 

#@app.route("/agregarPersona",methods=["POST"]) #este se utiliza es para utilizar con el postman 
#def agregar():
    nuevaPersona = request.json.get("persona")
    listaPersonas.append(nuevaPersona)
    return "Se agrego una nueva persona"

@app.route("/datosDeLaBase",methods=["GET"])
def datosBase():
    cursor.execute("SELECT * FROM persona")
    resultadosPersona = cursor.fetchall()
    return jsonify(resultadosPersona)

@app.route("/agregarPersonaBD",methods=["POST"])
def agregar():
    nuevaPersona = request.json.get("persona")
    listaPersonas.append(nuevaPersona) 
    cursor.execute("INSERT INTO persona(identificacion,nombre,edad) VALUES(%s,%s,%s)",
                   (nuevaPersona["identificacion"],nuevaPersona["nombre"],nuevaPersona["edad"]))
    db.commit()
    return "Se agrego una nueva persona"

@app.route("/buscarPersona/<identificacion>",methods=["GET"])
def buscar(identificacion):
    cursor.execute("SELECT * FROM persona WHERE identificacion = %s",(identificacion))
    resultadosDePersonas= cursor.fetchall()
    return jsonify(resultadosDePersonas)

@app.route("/actualizarPersona/<identificacion>", methods=["PUT"])
def actualizar(identificacion):
    datos_nuevos= request.json
    cursor.execute("UPDATE persona SET  nombre=%s,edad=%s, WHERE identificacion=%s",
    (datos_nuevos["nombre"],datos_nuevos["edad"],datos_nuevos["identificacion"]))
    db.commit()
    return "Persona actualizada"

@app.route("/eliminarPersona/<identificacion>",methods=["DELETE"])
def eliminar(identificacion):
    cursor.execute("DELETE FROM persona WHERE identificacion=%s",
    (identificacion,))
    db.commit()
    return "Persona eliminada"

if __name__ == "__main__":
   app.run(debug=True)

