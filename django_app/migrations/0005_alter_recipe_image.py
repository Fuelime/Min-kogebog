# Generated by Django 4.2.3 on 2023-08-06 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0004_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='', upload_to='images/'),
        ),
    ]
