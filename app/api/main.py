from flask import Flask, Response
from flask.globals import request
from flask_cors import CORS
from Mensaje_DAO import Mensaje_DAO
from datetime import datetime
import os
import shutil
# disable=redefined-outer-name

app = Flask(__name__)
mensaje = Mensaje_DAO()
CORS(app)

@app.route('/api/grabarMensajes/', methods=['POST'])
def grabar_mensajes():
    try:
        url_config = 'app/src/config.xml'
        shutil.copy(url_config, 'app/src/config_old.xml')
    except IOError:
        print('No se pudo copiar el archivo config.xml')
    
    file_mensaje = request.files['mensajes']
    file_config = request.files['config']
    
    if file_mensaje.filename != '' or file_config.filename != '':
        filename_mensaje = os.path.join(os.getcwd(), 'app', 'src', 'mensajes.xml')
        filename_config = os.path.join(os.getcwd(), 'app', 'src', 'config.xml')
        file_mensaje.save(filename_mensaje)
        file_config.save(filename_config)
        return 'Contenido guardado', 200
    
    return 'No hay archivo para analizar', 100


@app.route('/api/devolverHashtags/<fecha_inicial>/<fecha_final>', methods=['GET'])
def get_hashtags_date_range(fecha_inicial, fecha_final):    
    fecha_inicio = datetime.strptime(fecha_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
    fecha_fin = datetime.strptime(fecha_final, '%Y-%m-%d').strftime('%d/%m/%Y')

    datos = mensaje.get_hash_date_range(fecha_inicio, fecha_fin)
    return datos
    
@app.route('/api/devolverMenciones/<fecha_inicial>/<fecha_final>', methods=['GET'])
def get_menciones_date_range(fecha_inicial, fecha_final):
    fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
    fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d').strftime('%d/%m/%Y')
    
    datos = mensaje.get_menciones_date_range(fecha_inicial, fecha_final)
    return datos
    
@app.route('/api/devolverSentimientos/<fecha_inicial>/<fecha_final>', methods=['GET'])
def get_sentimientos_date_range(fecha_inicial, fecha_final):
    fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
    fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d').strftime('%d/%m/%Y')
    
    datos = mensaje.get_sentimientos_date_range(fecha_inicial, fecha_final)
    return datos

@app.route('/api/graficarHashtags/<fecha_inicial>/<fecha_final>', methods=['GET'])
def graficar_hashtags(fecha_inicial, fecha_final):
    if request.method == 'GET':
        fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
        fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d').strftime('%d/%m/%Y')
        pdf = mensaje.graficar_hashtags(fecha_inicial, fecha_final)
        return Response(pdf, mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=grafico_hashtag.pdf'})
    
@app.route('/api/graficarMenciones/<fecha_inicial>/<fecha_final>', methods=['GET'])
def graficar_menciones(fecha_inicial, fecha_final):
    if request.method == 'GET':
        fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
        fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d').strftime('%d/%m/%Y')
        pdf = mensaje.graficar_menciones(fecha_inicial, fecha_final)
        return Response(pdf, mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=grafico_menciones.pdf'})
    
@app.route('/api/graficarSentimientos/<fecha_inicial>/<fecha_final>', methods=['GET'])
def graficar_sentimientos(fecha_inicial, fecha_final):
    if request.method == 'GET':
        fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
        fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d').strftime('%d/%m/%Y')
        pdf = mensaje.graficar_sentimientos(fecha_inicial, fecha_final)
        return Response(pdf, mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=grafico_sentimientos.pdf'})

@app.route('/api/resumenMensajes/', methods=['GET'])
def resumen_mensajes():
    if request.method == 'GET':
        xml = mensaje.resumen_mensajes()
        return Response(xml, mimetype='application/xml', headers={'Content-Disposition': 'attachment;filename=resumen_mensajes.xml'})

@app.route('/api/resumenConfig/', methods=['GET'])
def resumen_config():
    if request.method == 'GET':        
        
        
        xml = mensaje.resumen_config()  
        return Response(xml, mimetype='application/xml', headers={'Content-Disposition': 'attachment;filename=resumen_config.xml'})

@app.route('/api/resetearDatos/', methods=['POST'])
def resetear_datos():
    if request.method == 'POST':
        mensaje.resetear_datos()
        return 'Datos reseteados.', 200

if __name__ == '__main__':
    app.run(debug=True)