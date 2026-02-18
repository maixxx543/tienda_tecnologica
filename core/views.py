from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def catalogo(request):
    return render(request, 'core/catalogo.html')

def formulario_registro(request):
    return render(request, 'core/formulario_registro.html')

def formulario_inicio_sesion(request):
    return render(request, 'core/formulario_inicio_sesion.html')


class ProductCreateView(View):
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
        return redirect('catalogo', category_id=1)


class ProductListView(View):
    template_name = 'core/catalogo.html'

    def get(self, request, category_id, *args, **kwargs):
        products = Product.objects.filter(category=category_id)
        return render(request, self.template_name, {'products': products})

class ProductDetailView(View):
    template_name = 'core/product_detail.html'

    def get(self, request, id, *arg, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'p': product})
    
class ProductUpdateView(View):
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
        return redirect('catalogo', category_id=1)

class ProductDeleteView(View):
    template_name = "core/product_confirm_delete.html"

    def get(self, request, id, *arg, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'product': product})
    
    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        product.delete()

        return redirect('catalogo', category_id=1)


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


class AddProduct(View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})
        product_id = str(pk)
        if product_id in cart:
            cart [product_id] += 1
        else:
            cart[product_id] = 1
        request.sessions('cart') == cart
        return redirect('catalogo')
    
# class CheckoutView(View):
#     def post(self, request):
#         cart = request.session.get('cart', {})
#         if not cart:
#             return redirect('catalogo')
        
#         order = Order.objects.create(
#             user=request.user,
#             status='pending',
#             payment_amount=0
#         )
#         total_final = 0

#         cart.items():
#         product = Product.objects.get(pk = pid)

#         OrderItem.objects.create(
#             order=order,
#             product=product,
#             quantity=qty
#         )
#         total_final += (product.price * qty)
#         order.payment_amount = total_final

#         order.save