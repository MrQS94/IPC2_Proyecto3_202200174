from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cargar_archivos', views.cargar_archivos, name='cargar_archivos'),
    path('peticiones_consultar_hashtags', views.peticiones_consultar_hashtags, name='peticiones_consultar_hashtags'),
    path('peticiones_consultar_menciones', views.peticiones_consultar_menciones, name='peticiones_consultar_menciones'),
    path('peticiones_consultar_sentimientos', views.peticiones_consultar_sentimientos, name='peticiones_consultar_sentimientos'),
    path('graficar_hashtags', views.graficar_hashtags, name='graficar_hashtags'),
    path('graficar_menciones', views.graficar_menciones, name='graficar_menciones'),
    path('graficar_sentimientos', views.graficar_sentimientos, name='graficar_sentimientos'),
    path('resumen_mensajes', views.resumen_mensajes, name='resumen_mensajes'),
    path('resumen_config', views.resumen_config, name='resumen_config'),
    path('resetear_datos', views.resetear_datos, name='resetear_datos'),
    path('ayuda', views.ayuda, name='ayuda'),
] 
