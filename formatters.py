def format_db_user (usuario):
    usuario_obj = {}
    usuario_obj["id"]               = usuario[0]
    usuario_obj["nombre"]           = usuario[1]
    usuario_obj["apellido_p"]       = usuario[2]
    usuario_obj["apellido_m"]       = usuario[3]
    usuario_obj["telefono"]         = usuario[4]
    usuario_obj["email"]            = usuario[5]
    usuario_obj["password"]         = usuario[6]
    usuario_obj["direccion"]        = usuario[7]
    usuario_obj["status_conectado"] = usuario[8]
    return usuario_obj

def format_db_pet (mascota):
    mascota_obj = {}
    mascota_obj["id"]               = mascota[0]
    mascota_obj["nombre"]           = mascota[1]
    mascota_obj["id_raza"]          = mascota[2]
    mascota_obj["color"]            = mascota[3]
    mascota_obj["descripcion"]      = mascota[4]
    mascota_obj["nacimiento"]       = mascota[5]
    mascota_obj["genero"]           = mascota[6]
    mascota_obj["id_status"]        = mascota[7]
    mascota_obj["id_usuario"]       = mascota[8]
    return mascota_obj

def format_db_address (direccion):
    direccion_obj = {}
    direccion_obj["id"]             = direccion[0]
    direccion_obj["calle"]          = direccion[1]
    direccion_obj["colonia"]        = direccion[2]
    direccion_obj["num_interior"]   = direccion[3]
    direccion_obj["num_exterior"]   = direccion[4]
    direccion_obj["codigo_postal"]  = direccion[5]
    direccion_obj["id_estado"]      = direccion[6]
    return direccion_obj

def format_db_state (estado):
    estado_obj = {}
    estado_obj["id"]                = estado[0]
    estado_obj["nombre"]            = estado[1]
    estado_obj["id_pais"]           = estado[2]
    return estado_obj

def format_db_breed (raza):
    raza_obj = {}
    raza_obj["id"]                = raza[0]
    raza_obj["nombre"]            = raza[1]
    return raza_obj

def format_db_status (status):
    status_obj = {}
    status_obj["id"]                = status[0]
    status_obj["nombre"]            = status[1]
    return status_obj