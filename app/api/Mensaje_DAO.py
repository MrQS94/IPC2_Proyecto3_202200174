from Mensaje import Mensaje
import xml.etree.ElementTree as ET
import re
from datetime import datetime
import json
import matplotlib.pyplot as plt
from io import BytesIO
import xml.dom.minidom as minidom
import os

class Mensaje_DAO():
    def __init__(self) :
        self.mensajes = []
        self.negativos = []
        self.positivos = []
        self.hashtags = []
        self.old_negativos = []
        self.old_positivos = []
        self.tildes = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
        }
        
    def procesar_mensaje(self):
        mensajes = ET.parse('./app/src/mensajes.xml').getroot()
        config = ET.parse('./app/src/config.xml').getroot()
        
        for positivo in config.find('sentimientos_positivos'):
            self.positivos.append(positivo.text)
        
        for negativo in config.find('sentimientos_negativos'):
            self.negativos.append(negativo.text)
        
        for mensaje in mensajes.findall('MENSAJE'):
            texto = mensaje.find('TEXTO').text.replace(',', ' ')
            fecha_lugar = mensaje.find('FECHA').text
            fecha = re.search(r'\d{2}/\d{2}/\d{4}', fecha_lugar).group()
            
            texto = ''.join(self.tildes.get(letra, letra) for letra in texto).lower()
            nuevo_mensaje = Mensaje(texto, fecha)
            self.mensajes.append(nuevo_mensaje)    
    
    def procesar_old_config(self):
        config = ET.parse('./app/src/config_old.xml').getroot()
        
        for positivo in config.find('sentimientos_positivos'):
            self.old_positivos.append(positivo.text)
        
        for negativo in config.find('sentimientos_negativos'):
            self.old_negativos.append(negativo.text)
    
    def inicializar(self):
        self.mensajes = []
        self.positivos = []
        self.negativos = []
        self.procesar_mensaje()
    
    def get_hash_date_range(self, fecha_inicio, fecha_final):
        self.inicializar()
        
        response = []
        for mensaje in self.mensajes:
            if self.parse_fecha(mensaje.fecha) >= self.parse_fecha(fecha_inicio) and self.parse_fecha(mensaje.fecha) <= self.parse_fecha(fecha_final):
                hashtags = re.findall(r'#\w+#', mensaje.texto)
                for hasht in hashtags:
                    response.append(hasht)
        contador_hashtags = {}
        for i in response:
            if i in contador_hashtags:
                contador_hashtags[i] += 1
            else:
                contador_hashtags[i] = 1
        datos_fecha = {
        'fecha_inicio': fecha_inicio,
        'fecha_final': fecha_final
        }
        
        resultado = datos_fecha.copy()
        resultado.update(contador_hashtags)
        
        return json.dumps([{hashtag: contador} for hashtag, contador in resultado.items()], indent=4).replace('\n', '')
    
    def get_menciones_date_range(self, fecha_inicio, fecha_final):
        self.inicializar()
        
        response = []
        for mensaje in self.mensajes:
            if self.parse_fecha(mensaje.fecha) >= self.parse_fecha(fecha_inicio) and self.parse_fecha(mensaje.fecha) <= self.parse_fecha(fecha_final):
                menciones = re.findall(r'@\w+', mensaje.texto)
                for mencion in menciones:
                    response.append(mencion)
        contador_menciones = {}
        for i in response:
            if i in contador_menciones:
                contador_menciones[i] += 1
            else:
                contador_menciones[i] = 1
        datos_fecha = {
        'fecha_inicio': fecha_inicio,
        'fecha_final': fecha_final
        }
        
        resultado = datos_fecha.copy()
        resultado.update(contador_menciones)
        
        return json.dumps([{menciones: contador} for menciones, contador in resultado.items()], indent=4).replace('\n', '')
    
    def get_sentimientos_date_range(self, fecha_inicio, fecha_final):
        self.inicializar()
        
        count_positivos = 0
        count_negativos = 0
        count_neutro = 0
        list_count_positivos = 0
        list_count_negativos = 0
        list_count_neutro = 0
        for mensaje in self.mensajes:
            if self.parse_fecha(mensaje.fecha) >= self.parse_fecha(fecha_inicio) and self.parse_fecha(mensaje.fecha) <= self.parse_fecha(fecha_final):
                
                for positivo in self.positivos:
                    count_positivos += str(mensaje.texto).count(positivo)
                for negativo in self.negativos:
                    count_negativos += str(mensaje.texto).count(negativo)
                if count_positivos == count_negativos:
                    count_neutro += 1
                
                list_count_positivos += count_positivos
                list_count_negativos += count_negativos
                list_count_neutro += count_neutro
                
                count_positivos = 0
                count_negativos = 0
                count_neutro = 0
        datos = {
            'Mensajes con sentimiento positivo': list_count_positivos,
            'Mensajes con sentimiento negativo': list_count_negativos,
            'Mensajes neutros': list_count_neutro
        }
        return datos
    
    def parse_fecha(self, fecha):
        return datetime.strptime(fecha, '%d/%m/%Y')
    
    def graficar_hashtags(self, fecha_inicial, fecha_final):
        self.inicializar()
        response = []
        for mensaje in self.mensajes:
            if self.parse_fecha(mensaje.fecha) >= self.parse_fecha(fecha_inicial) and self.parse_fecha(mensaje.fecha) <= self.parse_fecha(fecha_final):
                hashtags = re.findall(r'#\w+#', mensaje.texto)
                for hasht in hashtags:
                    response.append(hasht)
        contador_hashtags = {}
        for i in response:
            if i in contador_hashtags:
                contador_hashtags[i] += 1
            else:
                contador_hashtags[i] = 1
        
        # Separar hashtags y sus valores en listas separadas
        hashtags_list = contador_hashtags.keys()
        count_list = contador_hashtags.values()
        # Graficar los datos
        plt.figure(figsize=(10, 8))
        plt.bar(hashtags_list, count_list, color='skyblue')
        plt.xlabel('Hashtags')
        plt.ylabel('Cantidad')
        plt.title('Recuento de Hashtags')
        plt.xticks(rotation=45)  # Rotar etiquetas del eje x para una mejor visualización
        pdf = BytesIO()
        plt.savefig(pdf, format='pdf')
        pdf.seek(0)
        plt.close()
        return pdf
    
    def graficar_menciones(self, fecha_inicial, fecha_final):
        self.inicializar()
        response = []
        for mensaje in self.mensajes:
            if self.parse_fecha(mensaje.fecha) >= self.parse_fecha(fecha_inicial) and self.parse_fecha(mensaje.fecha) <= self.parse_fecha(fecha_final):
                menciones = re.findall(r'@\w+', mensaje.texto)
                for hasht in menciones:
                    response.append(hasht)
        contador_menciones = {}
        for i in response:
            if i in contador_menciones:
                contador_menciones[i] += 1
            else:
                contador_menciones[i] = 1
        
        # Separar hashtags y sus valores en listas separadas
        hashtags_list = contador_menciones.keys()
        count_list = contador_menciones.values()
        # Graficar los datos
        plt.figure(figsize=(10, 8))
        plt.bar(hashtags_list, count_list, color='skyblue')
        plt.xlabel('Menciones')
        plt.ylabel('Cantidad')
        plt.title('Recuento de Menciones')
        plt.xticks(rotation=45)  # Rotar etiquetas del eje x para una mejor visualización
        pdf = BytesIO()
        plt.savefig(pdf, format='pdf')
        pdf.seek(0)
        plt.close()
        return pdf
    
    def graficar_sentimientos(self, fecha_inicial, fecha_final):
        contador_menciones = self.get_sentimientos_date_range(fecha_inicial, fecha_final)
        
        # Separar hashtags y sus valores en listas separadas
        hashtags_list = contador_menciones.keys()
        count_list = contador_menciones.values()
        # Graficar los datos
        plt.figure(figsize=(10, 8))
        plt.bar(hashtags_list, count_list, color='skyblue')
        plt.xlabel('Palabras')
        plt.ylabel('Cantidad')
        plt.title('Recuento de Palabras')
        plt.xticks(rotation=45)  # Rotar etiquetas del eje x para una mejor visualización
        pdf = BytesIO()
        plt.savefig(pdf, format='pdf')
        pdf.seek(0)
        plt.close()
        return pdf
    
    def contar_msj_recibidos(self, fecha):
        self.inicializar()
        contador = 0
        for mensaje in self.mensajes:
            if mensaje.fecha == fecha:
                contador += 1
        return contador
    
    def contar_user_mencionados(self, fecha):
        self.inicializar()
        contador = 0
        for mensaje in self.mensajes:
            if mensaje.fecha == fecha:
                menciones = re.findall(r'@\w+', mensaje.texto)
                for _ in menciones:
                    contador += 1
        return contador
    
    def contar_hashtags(self, fecha):
        self.inicializar()
        contador = 0
        for mensaje in self.mensajes:
            if mensaje.fecha == fecha:
                hashtags = re.findall(r'#\w+#', mensaje.texto)
                for _ in hashtags:
                    contador += 1
        return contador
    
    def resumen_mensajes(self):
        self.inicializar()
        
        mensajes_recibidos = ET.Element('MENSAJES_RECIBIDOS')
        datos_por_fecha = {}  # Un diccionario para almacenar datos por fecha
        for mensaje in self.mensajes:
            fecha = mensaje.fecha
            if fecha not in datos_por_fecha:
                datos_por_fecha[fecha] = {
                    'msj_recibidos': self.contar_msj_recibidos(fecha),
                    'user_mencionados': self.contar_user_mencionados(fecha),
                    'hashtags_incluidos': self.contar_hashtags(fecha)
                }
        
        for fecha, datos in datos_por_fecha.items():
            tiempo = ET.SubElement(mensajes_recibidos, 'TIEMPO')
            fecha_elem = ET.SubElement(tiempo, 'FECHA')
            fecha_elem.text = str(fecha)
            msj_recibidos = ET.SubElement(tiempo, 'MSJ_RECIBIDOS')
            msj_recibidos.text = str(datos['msj_recibidos'])
            user_mencionados = ET.SubElement(tiempo, 'USR_MENCIONADOS')
            user_mencionados.text = str(datos['user_mencionados'])
            hash_incluidos = ET.SubElement(tiempo, 'HASH_INCLUIDOS')
            hash_incluidos.text = str(datos['hashtags_incluidos'])
            
        
        xml_str = ET.tostring(mensajes_recibidos, encoding='UTF-8')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml()
        
        return pretty_xml
    
    def contar_palabras_positivas(self):
        self.inicializar()
        contador = 0
        for cadena in self.mensajes:
            for char in cadena.texto.split():
                if char in self.positivos:
                    contador += 1
        return contador
    
    def contar_palabras_negativas(self):
        self.inicializar()
        contador = 0
        for cadena in self.mensajes:
            for char in cadena.texto.split():
                if char in self.negativos:
                    contador += 1
        return contador
    
    def contar_palabras_positivas_rechazadas(self):
        try:
            self.inicializar()
            self.procesar_old_config()
            contador = 0
            for cadena in self.mensajes:
                for char in cadena.texto.split():
                    if self.positivos and char in self.old_positivos:
                        contador += 1
            return contador
        except ValueError:
            return 0
        except FileNotFoundError:
            return 0
    
    def contar_palabras_negativas_rechazadas(self):
        try:
            self.inicializar()
            self.procesar_old_config()
            contador = 0
            for cadena in self.mensajes:
                for char in cadena.texto.split():
                    if self.negativos and char in self.old_negativos:
                        contador += 1
            return contador
        except ValueError:
            return 0
        except FileNotFoundError:
            return 0
    
    def resumen_config(self):
        self.inicializar()
        config_recibidos = ET.Element('CONFIG_RECIBIDA')
        
        palabras_positivas = ET.SubElement(config_recibidos, 'PALABRAS_POSITIVAS')
        palabras_positivas.text = str(self.contar_palabras_positivas())
        
        palabras_positivas = ET.SubElement(config_recibidos, 'PALABRAS_POSITIVAS_RECHAZADA')
        palabras_positivas.text = str(self.contar_palabras_positivas_rechazadas())
        
        palabras_negativas = ET.SubElement(config_recibidos, 'PALABRAS_NEGATIVAS')
        palabras_negativas.text = str(self.contar_palabras_negativas())
        
        palabras_positivas = ET.SubElement(config_recibidos, 'PALABRAS_NEGATIVAS_RECHAZADA')
        palabras_positivas.text = str(self.contar_palabras_negativas_rechazadas())
        
        xml_str = ET.tostring(config_recibidos, encoding='UTF-8')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml()
        
        return pretty_xml
    
    def resetear_datos(self):
        self.inicializar()
        self.mensajes = []
        self.positivos = []
        self.negativos = []
        self.hashtags = []
        self.tildes = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
        }
        os.remove('app/src/mensajes.xml')
        os.remove('app/src/config.xml')
        try:
            os.remove('app/src/config_old.xml')
        except FileNotFoundError:
            print('No se pudo eliminar el archivo config_old.xml')
    