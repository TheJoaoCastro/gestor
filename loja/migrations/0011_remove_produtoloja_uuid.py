# Generated by Django 5.1.3 on 2025-02-07 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0010_alter_loja_tipo_organizacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produtoloja',
            name='uuid',
        ),
    ]
