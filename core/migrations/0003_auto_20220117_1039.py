# Generated by Django 2.2.26 on 2022-01-17 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220115_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.IntegerField(help_text='Уникальный ID пользователя', verbose_name='ID пользователя'),
        ),
    ]