from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('',views.index, name='index'),
    path('catalogo/<int:replacement>',ProductListView.as_view(), name='catalogo'),
    #path('registro/',views.formulario_registro, name='formulario_registro'),
    path('login/', UserLoginView.as_view() ,name='login'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products_detail/<int:id>/', ProductDetailView.as_view(), name="product_detail"),
    path('products/<int:id>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:id>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    #path('carrito/', listcarrito.as_view(), name='carrito'),
    path('add/<int:pk>', AddProduct.as_view(), name='addproduct'),
    path('registro/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # URL para agregar productos (recibe el ID del producto)
    path('cart/add/<int:pk>/', AddProduct.as_view(), name='add_product'),
    
    # URL para ver la tabla del carrito y eliminar items (GET y POST)
    path('cart/', CartView.as_view(), name='cart_view'),
    
    # URL para procesar la orden y descontar stock
    path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
] 