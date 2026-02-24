from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help= "Sembrar datos iniciales en la base de datos de categoria"
    def handle(self, *args, **options):
        self.seed_categories()

    def seed_categories(self):
        categories = [
        {'name_category': "Telefono",'description': "Bonitos"},
        {'name_category': "Laptop", 'description': "De ultima generacion"}
    ]
        for category in categories:
            category , created = Category.objects.get_or_create(defaults=category, name_category=category['name_category'], description=category['description'])

            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoria: "{category.name_category}" creado.' ))
            else:
                self.stdout.write(self.style.WARNING(f'Categoria: "{category.name_category}" ha sido actualizada.'))