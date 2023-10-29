from django.shortcuts import render, HttpResponse
import requests
from django.http import JsonResponse, FileResponse

# Create your views here.
API_LINK = 'http://127.0.0.1:5000/api'

def home(request):
    return render(request, "home.html")

def cargar_archivos(request):
    if request.method == 'POST' and request.FILES['archivo_mensajes'] and request.FILES['archivo_config']:
        file_mensaje = request.FILES['archivo_mensajes']   
        file_config = request.FILES['archivo_config'] 
        
        archivos = {'mensajes': file_mensaje, 'config': file_config}
        response = requests.post(API_LINK + '/grabarMensajes/', files=archivos, timeout=200)
        if response.status_code == 200:
            return HttpResponse('Archivos cargados correctamente.')
        else:
            return HttpResponse('Error al cargar los archivos.')
        
    return render(request, "cargar_archivo_config.html")

def peticiones_consultar_hashtags(request):
    if request.method == 'GET':
        fecha_inicio = request.GET.get('fecha_inicial')
        fecha_final = request.GET.get('fecha_final')
        
        url = f'{API_LINK}/devolverHashtags/{fecha_inicio}/{fecha_final}'
        response = requests.get(url, timeout=200)
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        
    return render(request, "consultar_hash.html")

def peticiones_consultar_menciones(request):
    if request.method == 'GET':
        fecha_inicio = request.GET.get('fecha_inicial')
        fecha_final = request.GET.get('fecha_final')
        
        url = f'{API_LINK}/devolverMenciones/{fecha_inicio}/{fecha_final}'
        response = requests.get(url, timeout=200)
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        
    return render(request, "consultar_menciones.html")

def peticiones_consultar_sentimientos(request):
    if request.method == 'GET':
        fecha_inicio = request.GET.get('fecha_inicial')
        fecha_final = request.GET.get('fecha_final')
        
        url = f'{API_LINK}/devolverSentimientos/{fecha_inicio}/{fecha_final}'
        response = requests.get(url, timeout=200)
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        
    return render(request, "consultar_sentimientos.html")

def graficar_hashtags(request):
    if request.method == 'GET':
        fecha_inicio = request.GET.get('fecha_inicial')
        fecha_final = request.GET.get('fecha_final')
        
        url = f'{API_LINK}/graficarHashtags/{fecha_inicio}/{fecha_final}'
        response = requests.get(url, timeout=200)
        if response.status_code == 200:
            return FileResponse(response, content_type='application/pdf')
    return render(request, "graficar.html")

def graficar_menciones(request):
    if request.method == 'GET':
        fecha_inicio = request.GET.get('fecha_inicial')
        fecha_final = request.GET.get('fecha_final')
        
        url = f'{API_LINK}/graficarMenciones/{fecha_inicio}/{fecha_final}'
        response = requests.get(url, timeout=200)
        if response.status_code == 200:
            return FileResponse(response, content_type='application/pdf')
    return render(request, "graficar.html")

def graficar_sentimientos(request):
    if request.method == 'GET':
        fecha_inicio = request.GET.get('fecha_inicial')
        fecha_final = request.GET.get('fecha_final')
        
        url = f'{API_LINK}/graficarSentimientos/{fecha_inicio}/{fecha_final}'
        response = requests.get(url, timeout=200)
        if response.status_code == 200:
            return FileResponse(response, content_type='application/pdf')
    return render(request, "graficar.html")

def resumen_mensajes(request):
    if request.method == 'GET':
        url = f'{API_LINK}/resumenMensajes/'
        response = requests.get(url, timeout=200)
        if response.status_code == 200:
            return FileResponse(response, content_type='application/xml')

def resumen_config(request):
    if request.method == 'GET':
        url = f'{API_LINK}/resumenConfig/'
        response = requests.get(url, timeout=200)
        if response.status_code == 200:
            return FileResponse(response, content_type='application/xml')

def resetear_datos(request):
    if request.method == 'POST':
        url = f'{API_LINK}/resetearDatos/'
        response = requests.post(url, timeout=200)
        if response.status_code == 200:
            return HttpResponse('Datos reseteados correctamente.')
    return render(request, "resetear_datos.html")

def ayuda(request):
    return render(request, "ayuda.html")
