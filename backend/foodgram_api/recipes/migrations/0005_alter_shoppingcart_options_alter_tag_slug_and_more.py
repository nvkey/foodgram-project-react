# Generated by Django 4.0.6 on 2022-07-22 10:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Список покупок', 'verbose_name_plural': 'Списки покупок'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Only ^[-a-zA-Z0-9_]+$', regex='^[-a-zA-Z0-9_]+$')]),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_recipe'),
        ),
        migrations.AddConstraint(
            model_name='tagsrecipe',
            constraint=models.UniqueConstraint(fields=('tag', 'recipe'), name='unique_slug_recipe'),
        ),
    ]
