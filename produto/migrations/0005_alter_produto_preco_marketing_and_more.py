# Generated by Django 5.0.6 on 2024-06-03 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_produto_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='preco_marketing',
            field=models.FloatField(default=0, verbose_name='preço'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='preco_marketing_promocao',
            field=models.FloatField(default=0, verbose_name='preço promo'),
        ),
    ]
