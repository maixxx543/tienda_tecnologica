from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')
def catalogo(request):
    return render(request, 'core/catalogo.html')