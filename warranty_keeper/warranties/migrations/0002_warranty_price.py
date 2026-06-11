from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warranties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='warranty',
            name='price',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Purchase price of the item.',
                max_digits=10,
                null=True,
            ),
        ),
    ]
