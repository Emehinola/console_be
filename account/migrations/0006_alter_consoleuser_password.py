# Generated by Django 4.2.3 on 2023-07-08 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_consoleuser_groups_consoleuser_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consoleuser',
            name='password',
            field=models.CharField(max_length=500),
        ),
    ]