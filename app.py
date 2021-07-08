# # incluimos todo lo necesario para hacer el renderizado de
# # template y uso de flask
# from flask import Flask
# from flask import render_template
# app=Flask(__name__) # aca creamos la aplicacion
# @app.route('/') # cuando el usuario escriba / se va a buscar el

# # archivo index.html

# def index():
#     return render_template('empleados/index.html')
# if __name__=='__main__': # para que python pueda interpretar como

# # empezar a correr la aplicacion

#     app.run(debug=True) # va ejecurar la aplicacion y en modo debug
    
# from flask import Flask
# from flask import render_template
# from flaskext.mysql import MySQL

# app=Flask(__name__)
# mysql = MySQL

# app.config['MYSQL_DATABASE_HOST']='localhost'
# app.config['MYSQL_DATABASE_USER']='root'
# app.config['MYSQL_DATABASE_PASSWORD']=''

from flask import Flask
from flask import render_template, request ,redirect,url_for
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory #Acceso a las carpetas
import os #Nos pemite acceder a los archivos
app=Flask(__name__)
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_Db']='sistema'
mysql.init_app(app)

CARPETA= os.path.join('uploads') #Referencia a la carpeta
app.config['CARPETA']=CARPETA #Indicamos que vamos a guardar esta ruta de la carpeta


@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

@app.route('/')
def index():
    sql="SELECT * FROM `sistema`.`empleados`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall() #Traemos toda la información
    # print(empleados)
    conn.commit()
    return render_template('empleados/index.html' ,  empleados=empleados)

@app.route('/destroy/<int:id>') #Recibe como parámetro el id del registro
def destroy(id):
 conn = mysql.connect() #Se conecta a la conexión mysql.init_app(app)
 cursor = conn.cursor() #Almacenaremos lo que ejecutamos
 cursor.execute("DELETE FROM `sistema`.`empleados` WHERE id=%s", (id))
#En vez de pasarle el string la escribimos
 conn.commit() #Cerramos la conexión
 return redirect('/') #Regresamos de donde vinimos

@app.route('/edit/<int:id>') #Recibe como parámetro el id del registro
def edit(id):
    conn = mysql.connect() #Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor() #Almacenaremos lo que ejecutamos
    cursor.execute("SELECT * FROM `sistema`.`empleados` WHERE id=%s", (id)) #Ejecutamos la sentencia SQL sobre el id
    empleados=cursor.fetchall() #Traemos toda la información
    conn.commit() #Cerramos la conexión
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    id=request.form['txtID']
    sql = "UPDATE `sistema`.`empleados` SET `nombre`=%s, `correo`=%s WHERE id=%s;"
    datos=(_nombre,_correo,id)
    conn = mysql.connect() #Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor() #Almacenaremos lo que ejecutamos
    # Para ctualizar foto borrando la anterior y agregando la nueva tanto en la carpeta física como en la tabla    
    now= datetime.now()
    tiempo= now.strftime("%Y%H%M%S") #Años horas minutos y segundos
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename #Concatena el nombre
        _foto.save("uploads/"+nuevoNombreFoto) #Lo guarda en la carpeta
    cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s", id) #Buscamos la foto
    fila= cursor.fetchall() #Traemos toda la información
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0])) #Ese valor seleccionado se encuentra en la posición 0 y la fila 0
    cursor.execute("UPDATE `sistema`.`empleados` SET foto=%s WHERE id=%s", (nuevoNombreFoto, id)) #Buscamos la foto

    cursor.execute(sql,datos) #Ejecutamos la sentencia SQL
    conn.commit() #Cerramos la conexión
    return redirect('/')


@app.route('/create')
def create():
    return render_template('empleados/create.html')
@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    now= datetime.now()
    tiempo= now.strftime("%Y%H%M%S")
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename #Concatena el nombre
        _foto.save("uploads/"+nuevoNombreFoto)
    sql="INSERT INTO `sistema`.`empleados` (`nombre`, `correo`,`foto`) VALUES (%s,%s,%s);"
    datos=(_nombre,_correo,nuevoNombreFoto)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')
   

if __name__=='__main__':
    app.run(debug=True)
    
    
    


