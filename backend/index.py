from flask import Flask, render_template
from flask_cors import CORS
from flask import jsonify,request


app=Flask(__name__)
## Nos permite acceder desde una api externa
CORS(app)
## Funcion para conectarnos a la base de datos de mysql
def conectar(vhost,vuser,vpass,vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn
# Ruta para consulta general de mujeres cuidadoras
@app.route("/")
def index():
    titulo = "HOLA_MUNDO"
    return render_template, ("index.html" titulo=titulo)

@app.route("/index")
def consulta_general():
    try:
        conn=conectar('localhost','root','1234','manzanas_cuidadoras')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM mujer_cuidadora """)
        datos=cur.fetchall()
        data=[]
        for row in datos:
            dato={'idnumero_documento':row[0],'T_documento':row[1],'Nombres':row[2], 'apellidos':row[3],
                  'ciudad':row[4], 'n_celular':row[5], 'ocupacion':row[6], 'correo_electronico':row[7],
                  'servicios_gustaria':row[8], 'localidad':row[9]}
            data.append(dato)
        cur.close()
        conn.close()
        return render_template, jsonify("index.html")({'mujer_cuidadora':data,'mensaje':'registros encontrados'})
    except Exception as ex:
        return render_template, jsonify({'mensaje':'Error'})
    
## Ruta para hacer una consulta individual de las mujeres cuidadoras que estan 
# registradas en las manzanas del cuidado
@app.route("/consulta_individual/<codigo>",methods=['GET'])
def consulta_individual(codigo):
    try:
        conn=conectar('localhost','root','1234','manzanas_cuidadoras')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul where idnumero_documento='{0}' """.format(codigo))
        datos=cur.fetchone()
        cur.close()
        conn.close()
        if datos!=None:
            dato={'idnumero_documento':datos[0],'T_documento':datos[1],'Nombres':datos[2],'apellidos':datos[3],
                  'ciudad':datos[4], 'n_celular':datos[5], 'ocupacion':datos[6], 'correo_electronico':datos[7],
                  'servicios_gustaria':datos[8], 'localidad':datos[9]}
            return jsonify({'mujer_cuidadora':dato,'mensaje':'Registro encontrado'})  
        else:
            return jsonify({'mensaje':'Registro no encontrado'})     
    except Exception as ex:
        return jsonify({'mensaje':'Error'})
    
    
    ## ruta para hacer registro de las mujeress que quieran ingresar a manzanas cuidadoras
@app.route("/registro/",methods=['POST'])
def registro():
    try:
        conn=conectar('localhost','root','1234','manzanas_cuidadoras')
        cur = conn.cursor()
        x=cur.execute(""" insert into mujer_cuidadora (T_documento,Nombres,apellidos,ciudad,
                      n_celular,ocupacion,correo_electronico,servicios_gustaria,localidad) values \
            ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')""".format(request.json['plataforma'],\
                request.json['usuario'],request.json['clave']))
        conn.commit() ## Para confirmar la introduccion de la información 
        cur.close()
        conn.close()
        return jsonify({'mensaje':'Registro agregado'}) 
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'Error'})
    
        ## ruta para que las mujeres puedan eliminar su cuenta si ya no deseean pertenecer 
        # a las manzanas del cuidado
@app.route("/eliminar/<codigo>",methods=['DELETE'])
def eliminar(codigo):
    try:
        conn=conectar('localhost','root','1234','manzanas_cuidadoras')
        cur = conn.cursor()
        x=cur.execute(""" delete from baul where idnumero_documento={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje':'eliminado'}) 
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'Error'})
    
    ##ruta en lla que las mujeres puedan actualizar, editar o modificar su informacion de 
    # registro, ej: cambiaron de numero de telefono o de localidad
@app.route("/actualizar/<codigo>",methods=['PUT'])
def actualizar(codigo):
    try:
        conn=conectar('localhost','root','1234','manazanas_cuidadoras')
        cur = conn.cursor()
        x=cur.execute(""" update mujeres_cuidadoras set T_documento='{0}',Nombres='{1}',apellidos='{2}',
                      ciudad='{3}',n_celular='{4}',ocupacion='{5}','correo_electronico='{6}',
                      'servicios_gustaria='{6}',localidad='{7}' where \
            idnumero,documento={8}""".format(request.json['plataforma'],request.json['usuario'],\
                request.json['clave'],codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje':'Registro Actualizado'}) 
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'Error'})

if __name__=='__main__':
    app.run(debug=True)
