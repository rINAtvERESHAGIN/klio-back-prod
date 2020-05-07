from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0028_auto_20200505_0336'),
    ]

    operations = [
        TrigramExtension(),
    ]
