from django.shortcuts import render, redirect, get_object_or_404
from .models import Category,Product
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

        new_product = Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            description=description,
            replacement=replacement,
            category=category,
            image=image_file

        )
        return redirect('catalogo')

class ProductListView(View):
    template_name = 'core/catalogo.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
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
        return redirect('catalogo')

class ProductDeleteView(View):
    template_name = "core/product_confirm_delete.html"

    def get(self, request, id, *arg, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'product': product})
    
    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        product.delete()

        return redirect('catalogo')