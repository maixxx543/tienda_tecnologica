from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('catalogo/',views.catalogo, name='catalogo'),
    path('registro/',views.formulario_registro, name='formulario_registro'),
    path('inicio_sesion/',views.formulario_inicio_sesion, name='formulario_inicio_sesion'),
]