# Generated by Django 4.2.3 on 2023-07-09 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_consoleuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consoleuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
