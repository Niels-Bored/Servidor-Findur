from flask import Flask, request
from config import Config
from mysql import MySQL
from flask_cors import CORS
from formatters import format_db_user, format_db_pet, format_db_address, format_db_state, format_db_breed, format_db_status
from email_manager.sender import EmailManager
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL=os.getenv('EMAIL')
PASSWORD=os.getenv('PASSWORD')

EMAIL_MANAGER = EmailManager(EMAIL, PASSWORD)


app = Flask(__name__)
CORS(app)

# Obtener credentiales de base de datos
credentials = Config ()
db_server = credentials.get ("db_server")
db_name = credentials.get ("db_name")
db_user = credentials.get ("db_user")
db_password = credentials.get ("db_password")

# Conectar con mysql
database = MySQL (db_server, db_name, db_user, db_password)

###################################USUARIO################################################

@app.get("/usuarios/")
def get_usuarios ():
    """ Obetener usuarios """
    # Obtener todos los usuarios

    # Obtener offset
    offset = int(request.args.get ("offset", 0)) 
    
    # Inicializar lista vacía de usuarios 
    usuarios_list = []
    
    # Consultar información de base de datos
    usuarios = database.run_sql ("SELECT * FROM usuario")
    
    # Filtrar datos en base al offset
    usuarios = usuarios[offset:offset+20]
    
    # Recorrer cada usuario para convertirlo a un diccionario / objetos
    for usuario in usuarios: 
        
        # obtener y guardar usuario
        usuarios_list.append (format_db_user (usuario))
    
    # Retornar arreglo de objetos de usuarios
    return usuarios_list

@app.get("/usuario/<int:id>")
def get_usuario (id):
    """ Obetener usuario por id """
    
    # Consultar información de base de datos
    usuarios = database.run_sql (f"SELECT * FROM usuario WHERE id = {id}")
    if usuarios:
        
        # obtener usuario actual
        usuario = usuarios[0]
        usuario_obj = format_db_user (usuario)
        
        # Retornar arreglo de objetos de usuarios
        return usuario_obj

    else:
        return ({"error": "user not found"}, 403)

@app.post("/usuario/")
def post_usuario ():   
    """ Actualizar un usuario """ 
    
    # Obtener datos del requests
    id = request.json.get("id", "") 
    nombre = request.json.get("nombre", "")
    apellido_p = request.json.get("apellido_p", "") 
    apellido_m = request.json.get("apellido_m", "")
    telefono = request.json.get("telefono", "")
    email = request.json.get("email", "")  
    password = request.json.get("password", "")
    direccion = request.json.get("direccion", "")
    status_conectado = request.json.get("status_conectado", "") 
    
    if not id or not nombre or not apellido_p or not apellido_m or not telefono or not email or not password or not direccion or status_conectado=="":
        return ({"error": "invalid or missing pramaters"}, 403)

    # Verificar si usuario existe
    usuarios = database.run_sql (f"SELECT * FROM usuario WHERE id = {id}")
    if usuarios:
        # Actualizar usuario
        sql = f"UPDATE usuario SET nombre = '{nombre}', apellido_p = '{apellido_p}', apellido_m = '{apellido_m}', telefono = '{telefono}', email = '{email}', password = '{password}', direccion = {direccion}, status_conectado = {status_conectado} WHERE id = {id}"
        print(sql)
        database.run_sql (sql)
        
        return {"ok": True}

    else:
        return ({"error": f"user {id} not found"}, 403)   

@app.post("/usuario/login/")
def login ():   
    """ Login de usuario """ 
    
    # Obtener datos del requests
    nombre = request.json.get("nombre", "") 
    password = request.json.get("password", "")
    
    if not id or not nombre or not password:
        return ({"error": "invalid or missing pramaters"}, 403)

    # Verificar si usuario existe
    usuarios = database.run_sql (f"SELECT * FROM usuario WHERE nombre = '{nombre}' AND password = '{password}'")
    if usuarios:
        usuario = usuarios[0]
        return {"ok": True,"id": usuario[0]}

    else:
        return ({"error": f"Invalid credentials"}, 403)   

@app.post("/sendmail/")
def sendmail ():   
    """ Login de usuario """ 
    
    # Obtener datos del requests
    mail = request.json.get("mail", "") 
    body = request.json.get("body", "")
    
    if not mail or not body:
        return ({"error": "invalid or missing pramaters"}, 403)

    try:
        EMAIL_MANAGER.send_email([mail], 'Someone tried to contact you', body)
    except Exception as error: 
        print(error)
        return ({"error": error}, 500)  
    else: 
        return {"ok": True}
       

@app.put("/usuario/")
def put_usuario (): 
    """ Insertar un usuario """ 

    # Obtener datos del requests
    nombre = request.json.get("nombre", "")
    apellido_p = request.json.get("apellido_p", "") 
    apellido_m = request.json.get("apellido_m", "")
    telefono = request.json.get("telefono", "")
    email = request.json.get("email", "")  
    password = request.json.get("password", "")
    direccion = request.json.get("direccion", "")
    status_conectado = request.json.get("status_conectado", "") 
    
    if not nombre or not apellido_p or not apellido_m or not telefono or not email or not password or not direccion or not status_conectado:
        return ({"error": "invalid or missing pramaters"}, 403)


    # Insertar usuario en base de datos
    sql = f"""INSERT INTO usuario (
                nombre, 
                apellido_p,
                apellido_m,
                telefono,
                email,
                password, 
                direccion, 
                status_conectado) 
            VALUES ('{nombre}','{apellido_p}','{apellido_m}',{telefono},'{email}','{password}',{direccion},{status_conectado})"""
    print(sql)
    database.run_sql (sql)
    
    usuarios = database.run_sql (f"SELECT * FROM usuario WHERE nombre = '{nombre}' AND email = '{email}'")
    if usuarios:
        id = usuarios[0]
        print(id)
        return {"ok": True,"id": id[0]}

    else:
        return ({"error": f"there was an error on the insertion"}, 403)   
    
@app.delete("/usuario/<int:id>/")
def delete_usuario (id):
    """ Eliminar un usuario """ 

    # Obtener datos del requests
    #id = request.json.get("id", "") 

    if not id:
        return ({"error": "invalid or missing pramaters"}, 403)

    # Verificar si usuario existe
    usuarios = database.run_sql (f"SELECT * FROM usuario WHERE id = {id}")
    if usuarios:
        sql = f"DELETE FROM usuario WHERE id = {id}"
        database.run_sql (sql)
        return {"ok": True}
    else:
        return ({"error": f"user {id} not found"}, 403)

###################################MASCOTA################################################

@app.get("/mascotas/")
def get_mascotas ():
    """ Obetener mascotas """
    # Obtener todas las mascotas

    # Obtener offset
    offset = int(request.args.get ("offset", 0)) 
    
    # Inicializar lista vacía de mascotas
    mascotas_list = []
    
    # Consultar información de base de datos
    mascotas = database.run_sql ("SELECT * FROM mascota")
    
    # Filtrar datos en base al offset
    mascotas = mascotas[offset:offset+20]
    
    # Recorrer cada masctoa para convertirlo a un diccionario / objetos
    for mascota in mascotas: 
        
        # obtener y guardar usuario
        mascotas_list.append (format_db_pet (mascota))
    
    # Retornar arreglo de objetos de mascotas
    return mascotas_list

@app.get("/mascota/<int:id>")
def get_mascota (id):
    """ Obetener mascota por id """
    
    # Consultar información de base de datos
    mascotas = database.run_sql (f"SELECT * FROM mascota WHERE id = {id}")
    if mascotas:
        
        # obtener mascota actual
        mascota = mascotas[0]
        mascota_obj = format_db_pet (mascota)
        
        # Retornar arreglo de objetos de mascotas
        return mascota_obj

    else:
        return ({"error": "pet not found"}, 403)

@app.get("/mascota/usuario/<int:id>")
def get_mascotas_usuario (id):
    """ Obetener mascotas de un usuario por id """
    
    # Obtener offset
    offset = int(request.args.get ("offset", 0)) 
    
    # Inicializar lista vacía de mascotas
    mascotas_list = []
    
    # Consultar información de base de datos
    mascotas = database.run_sql (f"SELECT * FROM mascota WHERE id_usuario = {id}")
    
    # Filtrar datos en base al offset
    mascotas = mascotas[offset:offset+20]
    
    # Recorrer cada masctoa para convertirlo a un diccionario / objetos
    for mascota in mascotas: 
        
        # obtener y guardar usuario
        mascotas_list.append (format_db_pet (mascota))
    
    # Retornar arreglo de objetos de mascotas
    return mascotas_list

@app.post("/mascota/")
def post_mascota ():   
    """ Actualizar una mascota """ 
    
    # Obtener datos del requests
    id = request.json.get("id", "") 
    nombre = request.json.get("nombre", "")
    id_raza = request.json.get("id_raza", "") 
    color = request.json.get("color", "")
    descripcion = request.json.get("descripcion", "")
    genero = request.json.get("genero", "")
    id_status = request.json.get("id_status", "")
    id_usuario = request.json.get("id_usuario", "") 
    
    if not id or not nombre or not id_raza or not color or not descripcion or not genero or not id_status or not id_usuario:
        return ({"error": "invalid or missing pramaters"}, 403)

    # Verificar si mascota existe
    usuarios = database.run_sql (f"SELECT * FROM mascota WHERE id = {id}")
    if usuarios:
        # Actualizar mascota
        sql = f"UPDATE mascota SET nombre = '{nombre}', id_raza = '{id_raza}', color = '{color}', descripcion = '{descripcion}', genero = '{genero}', id_status = '{id_status}', id_usuario = '{id_usuario}' WHERE id = {id}"
        database.run_sql (sql)
        
        return {"ok": True}

    else:
        return ({"error": f"pet {id} not found"}, 403)   

@app.put("/mascota/")
def put_mascota (): 
    """ Insertar una mascota """

    # Obtener datos del requests 
    nombre = request.json.get("nombre", "")
    id_raza = request.json.get("id_raza", "") 
    color = request.json.get("color", "")
    descripcion = request.json.get("descripcion", "")
    nacimiento = request.json.get("nacimiento", "")  
    genero = request.json.get("genero", "")
    id_status = request.json.get("id_status", "")
    id_usuario = request.json.get("id_usuario", "") 
    
    if not nombre or not id_raza or not color or not descripcion or not nacimiento or not genero or not id_status or not id_usuario:
        return ({"error": "invalid or missing pramaters"}, 403)

    print(nacimiento)
    # Insertar mascota en base de datos
    sql = f"""INSERT INTO mascota (
                nombre, 
                id_raza,
                color,
                descripcion,
                nacimiento,
                genero, 
                id_status, 
                id_usuario) 
            VALUES ('{nombre}','{id_raza}','{color}','{descripcion}','{nacimiento}','{genero}',{id_status},{id_usuario})"""
    database.run_sql (sql)
    
    mascotas = database.run_sql (f"SELECT * FROM mascota WHERE nombre = '{nombre}' AND nacimiento = '{nacimiento}'")
    if mascotas:
        id = mascotas[0]
        print(id)
        return {"ok": True,"id": id[0]}

    else:
        return ({"error": f"there was an error on the insertion"}, 403)
    
@app.delete("/mascota/<int:id>")
def delete_mascota (id):
    """ Eliminar una mascota """

    # Obtener datos del requests
    #id = request.json.get("id", "") 
        
    if not id:
        return ({"error": "invalid or missing pramaters"}, 403)

    # Verificar si mascota existe
    usuarios = database.run_sql (f"SELECT * FROM mascota WHERE id = {id}")
    if usuarios:
        sql = f"DELETE FROM mascota WHERE id = {id}"
        database.run_sql (sql)
        return {"ok": True}
    else:
        return ({"error": f"pet {id} not found"}, 403)

###################################DIRECCION################################################

@app.get("/direccion/<int:id>/")
def get_direccion (id):
    """ Obetener direccion por id """
    
    # Consultar información de base de datos
    direcciones = database.run_sql (f"SELECT * FROM direccion WHERE id = {id}")
    if direcciones:
        
        # obtener direccion actual
        direccion = direcciones[0]
        direccion_obj = format_db_address (direccion)
        
        # Retornar arreglo de objetos de direcciones
        return direccion_obj

    else:
        return ({"error": "address not found"}, 403)

@app.post("/direccion/")
def post_direccion ():   
    """ Actualizar una direccion """ 
    
    # Obtener datos del requests
    id = request.json.get("id", "") 
    calle = request.json.get("calle", "")
    colonia = request.json.get("colonia", "") 
    num_interior = request.json.get("num_interior", "")
    num_exterior = request.json.get("num_exterior", "")
    codigo_postal = request.json.get("codigo_postal", "")  
    id_estado = request.json.get("id_estado", "")
    
    if not id or not calle or not colonia or not num_interior or not num_exterior or not codigo_postal or not id_estado:
        return ({"error": "invalid or missing pramaters"}, 403)

    # Verificar si direccion existe
    usuarios = database.run_sql (f"SELECT * FROM direccion WHERE id = {id}")
    if usuarios:
        # Actualizar usuario
        sql = f"UPDATE direccion SET calle = '{calle}', colonia = '{colonia}', num_interior = '{num_interior}', num_exterior = '{num_exterior}', codigo_postal = '{codigo_postal}', id_estado = '{id_estado}' WHERE id = {id}"
        database.run_sql (sql)
        
        return {"ok": True}

    else:
        return ({"error": f"address {id} not found"}, 403)   

@app.put("/direccion/")
def put_direccion (): 
    """ Insertar una direccion """

    # Obtener datos del requests
    calle = request.json.get("calle", "")
    colonia = request.json.get("colonia", "") 
    num_interior = request.json.get("num_interior", "")
    num_exterior = request.json.get("num_exterior", "")
    codigo_postal = request.json.get("codigo_postal", "")  
    id_estado = request.json.get("id_estado", "")
    
    if not calle or not colonia or not num_interior or not num_exterior or not codigo_postal or not id_estado:
        return ({"error": "invalid or missing pramaters"}, 403)

    # Insertar direccion en base de datos
    sql = f"""INSERT INTO direccion (
                calle, 
                colonia,
                num_interior,
                num_exterior,
                codigo_postal, 
                id_estado) 
            VALUES ('{calle}','{colonia}','{num_interior}',{num_exterior},{codigo_postal},'{id_estado}')"""
    database.run_sql (sql)

    direcciones = database.run_sql (f"SELECT * FROM direccion WHERE calle = '{calle}' AND colonia = '{colonia}'")
    if direcciones:
        id = direcciones[0]
        print(id)
        return {"ok": True,"id": id[0]}

    else:
        return ({"error": f"there was an error on the insertion"}, 403)   
    
@app.delete("/direccion/<int:id>/")
def delete_direccion (id): 
    """ Eliminar una direccion """

    # Obtener datos del requests
    #id = request.json.get("id", "") 
        
    if not id:
        return ({"error": "invalid or missing pramaters"}, 403)

    # Verificar si direccion existe
    usuarios = database.run_sql (f"SELECT * FROM direccion WHERE id = {id}")
    if usuarios:
        sql = f"DELETE FROM direccion WHERE id = {id}"
        database.run_sql (sql)
        return {"ok": True}
    else:
        return ({"error": f"address {id} not found"}, 403)

###################################MASCOTA################################################

@app.get("/estados/")
def get_estados ():
    """ Obetener estados """
    # Obtener todos los estados

    # Obtener offset
    offset = int(request.args.get ("offset", 0)) 
    
    # Inicializar lista vacía de estados
    estados_list = []
    
    # Consultar información de base de datos
    estados = database.run_sql ("SELECT * FROM estado")
    
    # Filtrar datos en base al offset
    estados = estados[offset:offset+20]
    
    # Recorrer cada masctoa para convertirlo a un diccionario / objetos
    for estado in estados: 
        
        # obtener y guardar usuario
        estados_list.append (format_db_state (estado))
    
    # Retornar arreglo de objetos de mascotas
    return estados_list

###################################RAZA################################################

@app.get("/razas/")
def get_razas ():
    """ Obetener razas """
    # Obtener todas las razas

    # Obtener offset
    offset = int(request.args.get ("offset", 0)) 
    
    # Inicializar lista vacía de razas
    razas_list = []
    
    # Consultar información de base de datos
    razas = database.run_sql ("SELECT * FROM raza")
    
    # Filtrar datos en base al offset
    razas = razas[offset:offset+20]
    
    # Recorrer cada masctoa para convertirlo a un diccionario / objetos
    for raza in razas: 
        
        # obtener y guardar raza
        razas_list.append (format_db_breed (raza))
    
    # Retornar arreglo de objetos de razas
    return razas_list

###################################STATUS################################################

@app.get("/status/")
def get_status ():
    """ Obetener status """
    # Obtener todos los status

    # Obtener offset
    offset = int(request.args.get ("offset", 0)) 
    
    # Inicializar lista vacía de status
    status_list = []
    
    # Consultar información de base de datos
    status = database.run_sql ("SELECT * FROM status_mascota")
    
    # Filtrar datos en base al offset
    status = status[offset:offset+20]
    
    # Recorrer cada masctoa para convertirlo a un diccionario / objetos
    for stat in status: 
        
        # obtener y guardar status
        status_list.append (format_db_breed (stat))
    
    # Retornar arreglo de objetos de razas
    return status_list

if __name__ == "__main__":
    app.run(port="3000", host="0.0.0.0", debug=True)