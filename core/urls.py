from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('',views.index, name='index'),
    path('catalogo/',ProductListView.as_view(), name='catalogo'),
    path('registro/',views.formulario_registro, name='formulario_registro'),
    path('inicio_sesion/',views.formulario_inicio_sesion, name='formulario_inicio_sesion'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products_detail/<int:id>/', ProductDetailView.as_view(), name="product_detail"),
    path('products/<int:id>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:id>/delete/', ProductDeleteView.as_view(), name='product_delete')
]