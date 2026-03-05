from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib.auth import authenticate,login,get_user_model,logout
from .forms import *
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def catalogo(request):
    return render(request, 'core/catalogo.html')

def formulario_registro(request):
    return render(request, 'core/formulario_registro.html')
    

#-------------------------------------------------------------------------------------
#   Crear Producto
#-------------------------------------------------------------------------------------
class ProductCreateView(LoginRequiredMixin ,View):
    template_name = 'core/registrar_producto.html'

    def get(self, request, *arg, **kwars):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})

    
    def post(self, request, *arg, **kwargs):
        name = request.POST.get("name")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        description = request.POST.get("description", "")
        replacement = request.POST.get("replacement")== "on"
        category_id = request.POST.get("category")
        category = Category.objects.filter(id=category_id).first() if category_id else None
        image_file = request.FILES.get('image')

        errors = {}

        if not name:
            errors['name'] = "El nombre es requerido"
        if price:
            numero = dir(price)
            print(numero)
            if not price.isdecimal():
                errors['price'] = "El precio es debe ser decimal"
        else:
            errors['price'] = "El precio es requerido"
        if not stock:
            errors['stock'] = "El stock es requerido"
        if not category:
            errors['category'] = "La categoria es requerida"
        if not image_file:
            errors['image_file'] = "La imagen es requerida"
        
        if errors:

            categories = Category.objects.all()
            return render(request, self.template_name, {
                'categories': categories,
                'errors': errors,
            })

        new_product = Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            description=description,
            replacement=replacement,
            category=category,
            image=image_file

        )
        return redirect('catalogo', replacement=0)


class ProductListView(View):
    template_name = 'core/catalogo.html'
    paginate_by = 4

    def get(self, request, replacement, *args, **kwargs):
        # Convierto replacement a int para asegurar comparaciones
        replacement = int(replacement)
        if replacement==1:
            products = Product.objects.filter(replacement=True, stock__gt=0)
        else:
            products = Product.objects.filter(replacement=False, stock__gt=0)
        query = request.GET.get('q')
        category = request.GET.get('category')

        if query:
            products = products.filter(name__icontains=query)

        if category:
            products = products.filter(category__id=category)

        paginator = Paginator(products, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        query_dict=request.GET.copy()
        if "page" in query_dict:
            del query_dict ["page"]
        url_params=query_dict.urlencode()

        context = {
            'page_obj': page_obj,
            'products': page_obj.object_list,
            'query': query,
            'categories': Category.objects.all(),
            'category': Category.objects.filter(id=category).first() if category else None,
            'url_params': url_params,
            'replacement': replacement
        }

        return render(request, self.template_name, context)


    

class ProductDetailView(View):
    template_name = 'core/product_detail.html'

    def get(self, request, id, *arg, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'p': product})
    
class ProductUpdateView(LoginRequiredMixin, View):
    template_name = 'core/product_update.html'

    def get(self,request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        categories = Category.objects.all()
        return render(request, self.template_name, {'product': product, 'categories': categories})

    
    def post(self, request, id, *arg, **kwargs):
        product = get_object_or_404(Product, id=id)

        name = request.POST.get("name")
        print(name)
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        description = request.POST.get("description", "")
        replacement = request.POST.get("replacement")== "on"
        category_id = request.POST.get("category")
        category = Category.objects.filter(id=category_id).first() if category_id else None
        new_image_file = request.FILES.get('image')
        
        if new_image_file:
            if product.image and product.image.name:
                product.image.delete(save=False)
                
            product.image = new_image_file
        
        product.name=name
        product.price=price
        product.stock=stock
        product.description=description
        product.replacement=replacement
        product.category=category
        
        product.save()
        return redirect('catalogo', replacement=0)

class ProductDeleteView(LoginRequiredMixin, View):
    template_name = "core/product_confirm_delete.html"

    def get(self, request, id, *arg, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'product': product})
    
    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        product.delete()

        return redirect('catalogo', replacement=0)


class CartView(View):
    template_name ='core/pedido.html'
    
    def get_context_data(self, request, *arg, **kwargs):

        context = super.get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        items= []
        total = 0 
        for pid,qty in cart.items():
            product = get_object_or_404(Product, pk = pid)

            subtotal = product.price*qty
            total += subtotal

            items.append({
                'product':product,
                'quantity':qty,
                'subtotal':subtotal,
            })

            context['items']= items
            context['total']= total
        return context
    
class UserLoginView(View):
    template_name = 'core/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('catalogo', replacement=0)
        form = LoginForm()
        return render(request, self.template_name,{'form': form})

        
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if request.user.is_authenticated:
            return redirect('catalogo', replacement=0)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('catalogo', replacement=0)
            else:
                return render(request,self.template_name, {
                    'form': form,
                    'error_message': 'nombre de usuario o contraseña incorrecto.'
                })
            
        return render(request, self.template_name, { 'form': form})

User = get_user_model()


class UserRegisterView(View):
    template_name = 'core/register.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        if request.user.is_authenticated:
            return redirect('catalogo', replacement=0)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if request.user.is_authenticated:
            return redirect('catalogo', replacement=0)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password)

            login(request, user)

            return redirect('catalogo', replacement=0)
        return render(request, self.template_name, {'form': form})
    

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    


class AddProduct(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})
        product_id = str(pk)
        product = get_object_or_404(Product, id=pk)
        
        # Guardamos la URL de donde viene el usuario antes de hacer nada
        next_url = request.META.get('HTTP_REFERER')

        # cantidad del carro si no existe es 0
        current_qty = cart.get(product_id, 0)

        if current_qty >= product.stock:
            # envio el mensaje que se muestra despues del redirect
            messages.error(request, f"Lo sentimos, no hay suficiente stock de {product.name}.")
            return redirect(next_url) if next_url else redirect('catalogo', replacement=0)

        cart[product_id] = current_qty + 1
        request.session['cart'] = cart
        request.session.modified = True
        
        # mensaje de compra exitosa
        messages.success(request, "Producto añadido al carrito.")

        #redirigir a la URL exacta
        if next_url:
            return redirect(next_url)
        
        return redirect('catalogo', replacement=0)
    
class CheckoutView(View):
    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('catalogo', replacement=0)
    
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    status='pending',
                    payment_amount=0
                )
                total_final = 0

                for pid, qty in cart.items():
                    product=Product.objects.get(pk=pid)
                    if product.stock < qty:
                        raise ValueError(f"no hay stock suficiente para {product.name}. Disponible: {product.stock}")
                
                    OrderItem.objects.create(
                        order=order, 
                        product=product, 
                        quantity=qty
                        )
                    total_final += (product.price*qty)
                    product.stock = F('stock') - qty
                    product.save()

                order.payment_amount=total_final
                order.save()
                request.session['cart']={}
        except ValueError as e:
                messages.error(request, str(e))
                return redirect('cart_view')
        return redirect('catalogo', replacement=0)
    

class CartView(LoginRequiredMixin, View):
    template_name = 'core/carrito.html'

    def get(self, request):
        # Obtenemos el carrito de la sesión { "id_producto": cantidad }
        cart_session = request.session.get('cart', {})
        products_list = []
        total_cart_price = 0

        # Buscamos cada producto en la DB para obtener nombre, precio e imagen
        for product_id, quantity in cart_session.items():
            product = get_object_or_404(Product, id=product_id)
            subtotal = product.price * quantity
            total_cart_price += subtotal
            
            # Creamos un objeto temporal para el template
            products_list.append({
                'id': product_id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'subtotal': subtotal,
                'image': product.image
            })

        context = {
            'products': products_list,
            'total_cart_price': total_cart_price,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Maneja eliminar productos o vaciar sesión"""
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})

        if action == 'remove' and product_id in cart:
            del cart[product_id]
        
        elif action == 'clear':
            cart = {}

        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart_view')