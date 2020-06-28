from django.core.management.base import BaseCommand
from django.db.models import Count

from products.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        dupes = Product.objects.values('slug').annotate(slug_count=Count('slug')).order_by().filter(slug_count__gt=1)
        for item in dupes:
            one_slug_dupes = Product.objects.filter(slug=item['slug'])
            for index, product in enumerate(one_slug_dupes):
                if index > 0:
                    product.slug = '{0}-{1}'.format(product.slug, index)
                    product.save()
