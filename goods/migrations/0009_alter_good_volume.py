# Generated by Django 4.2.4 on 2023-10-06 07:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("goods", "0008_good_volume"),
    ]

    operations = [
        migrations.AlterField(
            model_name="good",
            name="volume",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                max_digits=6,
                null=True,
                verbose_name="Объем, л",
            ),
        ),
    ]
