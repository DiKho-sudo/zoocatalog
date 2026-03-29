"""
Автоматическое распределение товаров по категориям на основе названия
"""

from django.core.management.base import BaseCommand
from products.models import Product, Category, AnimalType
from django.db.models import Q


class Command(BaseCommand):
    help = 'Автоматическое распределение товаров по категориям'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем распределение товаров по категориям...\n')
        
        # Правила распределения по категориям
        category_rules = {
            'suhie-korma': ['корм', 'сухой', 'adult', 'puppy', 'kitten', 'sirius', 'acana'],
            'vlazhnye-korma': ['консерв', 'паштет', 'желе', 'мусс'],
            'lakomstva': ['лакомство', 'снек', 'палочки'],
            
            'miski': ['миска', 'мисочка'],
            'kormushki': ['кормушка', 'автокормушка'],
            'poilki': ['поилка', 'фонтан'],
            'kontejnery': ['контейнер'],
            
            'tualety': ['туалет', 'toilet', 'лоток', 'домик'],
            'lotki': ['лоток'],
            'napolniteli': ['наполнитель'],
            'sovki': ['совок'],
            
            'mjagkie-igrushki': ['игрушка', 'плюш'],
            'mjachiki': ['мяч', 'мячик'],
            'kogteto chki': ['когтеточка', 'драпак'],
            
            'shampuni': ['шампунь'],
            'rascheski': ['расческа', 'щетка', 'фурминатор'],
            
            'oshejniki': ['ошейник'],
            'povodki': ['поводок'],
            'ruletki': ['рулетка', 'flexi'],
        }
        
        # Правила для типов животных
        animal_rules = {
            'koshki': ['кошк', 'кот', 'cat', 'felix', 'whiskas'],
            'sobaki': ['собак', 'пес', 'dog', 'pedigree', 'chappi'],
            'gryzuny': ['хомяк', 'крыс', 'мыш', 'кролик', 'грызун'],
            'ptitsy': ['птиц', 'попугай', 'канарейка'],
            'ryby': ['рыб', 'аквариум', 'aqua'],
        }
        
        categorized_count = 0
        animal_typed_count = 0
        
        products = Product.objects.all()
        total = products.count()
        
        for idx, product in enumerate(products, 1):
            if idx % 100 == 0:
                self.stdout.write(f'Обработано: {idx}/{total}')
            
            name_lower = product.name.lower()
            changed = False
            
            # Определяем категорию
            for cat_slug, keywords in category_rules.items():
                if any(keyword in name_lower for keyword in keywords):
                    try:
                        category = Category.objects.get(slug=cat_slug)
                        if product.category != category:
                            product.category = category
                            categorized_count += 1
                            changed = True
                        break
                    except Category.DoesNotExist:
                        pass
            
            # Определяем тип животного
            for animal_slug, keywords in animal_rules.items():
                if any(keyword in name_lower for keyword in keywords):
                    try:
                        animal = AnimalType.objects.get(slug=animal_slug)
                        if product.animal_type != animal:
                            product.animal_type = animal
                            animal_typed_count += 1
                            changed = True
                        break
                    except AnimalType.DoesNotExist:
                        pass
            
            if changed:
                product.save()
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('ИТОГИ:'))
        self.stdout.write(self.style.SUCCESS(f'Товаров распределено по категориям: {categorized_count}'))
        self.stdout.write(self.style.SUCCESS(f'Товаров распределено по типам животных: {animal_typed_count}'))
        self.stdout.write(self.style.SUCCESS('='*60))









