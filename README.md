# 💻 tienda Tech Market

## ✨ Descripción del Proyecto

Este proyecto es una plataforma de comercio electrónico diseñada para la venta y gestión de productos tecnológicos. Permite a los usuarios navegar por un catálogo actualizado de laptops, smartphones y componentes de hardware, ofreciendo una experiencia de compra fluida y segura.

Está orientado tanto a clientes finales como a técnicos que buscan repuestos específicos, con una interfaz moderna y un panel de administración robusto.

## ⚙️ Características Principales

- **✅ Catálogo Dinámico:** Visualización de productos filtrados por categorías (Laptops, Celulares, Repuestos).
- **✅ Gestión de Carrito:** Sistema funcional para añadir, eliminar y actualizar cantidades de productos.
- **✅ Autenticación de Usuarios:** Registro e inicio de sesión seguro para clientes.
- **✅ Panel Administrativo (Django Admin):** Gestión total de inventario, stock y pedidos.
- **✅ Buscador Inteligente:** Filtro rápido por nombre del producto.

## 🛠️ En Desarrollo

- **🔄 Pasarela de Pagos:** Integración con Stripe o PayPal.
- **📦 Seguimiento de Envíos:** Módulo para que el cliente vea el estado de su orden en tiempo real.
- **💬 Soporte vía WhatsApp:** Botón flotante para atención directa al cliente.

## 🚀 Tecnologías Utilizadas

El proyecto está construido utilizando un stack potente y escalable:

1. **HTML5 & CSS:** Estructura y diseño responsive (adaptable a móviles).
2. **Python 3.13:** Lenguaje de programación principal.
3. **Django 6.0.1:** Framework web para la lógica de negocio y seguridad.
4. **MySQL 2.2.7:** Base de datos robusta para el manejo de productos y usuarios.

## 📥 Instalación

Sigue estos pasos para ejecutar el proyecto localmente:

### 1. Clona el Repositorio

clona el repositorio desde GitHub

```bash
git clone https://github.com/maixxx543/tienda_tecnologica.git
cd tienda_tecnologica
  ```

### 2. Instalacion de archivos
- Creacion de entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
  ```
- Instalacion de librerias y dependencias
```bash
pip install -r requirements.txt
  ```

### 3. Ejecucion
- Verificar funcionalidad
```bash
python manage.py runserver
  ```
