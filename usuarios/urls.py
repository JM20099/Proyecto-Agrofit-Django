from django.urls import path
from . import views

urlpatterns = [
     path('', views.inicio, name="inicio"),
     path('registro/', views.registro, name="registro"),
     path('registro_correcto/', views.registro_correcto, name="registro_correcto"),
     path('home/', views.home, name="home"),
     path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
]