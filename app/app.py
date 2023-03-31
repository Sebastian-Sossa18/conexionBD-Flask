from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL

app = Flask (__name__)

#Conexión base de datos MYSQL
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='blog'

conexion = MySQL(app)

@app.before_request
def before_request():
    print('antes de la petición')

@app.after_request
def after_request(response):
    print('despues de la petición')
    return response

@app.route('/')
def index():

    usuario=['Pikachú', 'Charizard', 'Skutank', 'Pidgey', 'Onix']

    data={
          'titulo':'index',
          'bienvenida':'Pokémon',
          'usuario':usuario,
          'n_pokemons': 1 
    }
    return render_template('index.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre,edad):
    data={
        'titulo': 'contacto',
        'nombre': nombre,
        'edad': edad
    }

    return render_template('contacto.html', data=data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('usuario'))
    print(request.args.get('edad'))
    return "ok"

@app.route('/usuario')
def listar_usuarios():
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT id_usuario, nombre, email FROM usuarios ORDER BY id_usuario ASC" 
        cursor.execute(sql)
        usuarios=cursor.fetchall()
        #print(usuarios)
        data['usuario']=usuarios
        data['mensaje']='Éxito..'
    except Exception as ex:
        data['mensaje']='Error..'
    return jsonify(data)

def pagina_no_encontrada(error):
    #return render_template ('404.html'), 404
    return redirect(url_for('index'))



if __name__ =='__main__':
    app.add_url_rule('/query_string', view_func = query_string )
    app.register_error_handler(404, pagina_no_encontrada )
    app.run(debug=True,port=5000)