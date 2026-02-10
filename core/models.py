from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator



#-----------------------------------------------------
#   USUARIO
#-----------------------------------------------------
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["phone_number"]
    class Meta:
        db_table = "users"
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.username} ({self.email})"
    



#----------------------------------------------------------------
#   CATEGORY
#----------------------------------------------------------------
class Category(models.Model):
    name_category = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "categories"
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.name_category





#------------------------------------------------------------------------------------------------------
#   PRODUCTO
#----------------------------------------------------------------------------------------------------
class Product(models.Model): # Cambiado a Singular
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    replacement = models.BooleanField(default=False)
    image = models.ImageField(
        verbose_name='Imagen',
        upload_to='core/Product/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','webp'])],
        blank=True,
        null=True
    )

    class Meta:
        db_table = "products"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.image: # Revisa si el objeto tiene una imagen
            self.image.delete(save=False) # Borra el archivo físico en /media/
        super().delete(*args, **kwargs) # Borra el registro de la base de datos




#--------------------------------------------------------------------------------------------
#  PEDIDO
#----------------------------------------------------------------------------------------
class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('transfer', 'Bank Transfer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    
    class Meta:
        db_table = "orders"
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.status})"




#--------------------------------------------------------------------------------------------------
#   ARTICULO DE PEDIDO
#----------------------------------------------------------------------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2) 

    class Meta:
        db_table = "order_items"
        verbose_name = "Pedido item"
        verbose_name_plural = "Pedido items"
    

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    

