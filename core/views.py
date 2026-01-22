from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def catalogo(request):
    return render(request, 'core/catalogo.html')

def formulario_registro(request):
    return render(request, 'core/formulario_registro.html')

def formulario_inicio_sesion(request):
    return render(request, 'core/formulario_inicio_sesion.html')
