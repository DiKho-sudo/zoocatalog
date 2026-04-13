from django.core.management.base import BaseCommand

from products.models import Category


class Command(BaseCommand):
    help = "Fix known seed and catalog data issues."

    def handle(self, *args, **options):
        updates = {
            "sredstva-gigieny": {
                "name": "Средства гигиены",
                "description": "Средства гигиены для животных",
            },
        }

        fixed_count = 0

        for slug, values in updates.items():
            updated = Category.objects.filter(slug=slug).update(**values)
            fixed_count += updated
            if updated:
                self.stdout.write(self.style.SUCCESS(f"Updated category: {slug}"))
            else:
                self.stdout.write(f"Category not found, skipped: {slug}")

        self.stdout.write(self.style.SUCCESS(f"Done. Updated rows: {fixed_count}"))
