# Generated by Django 4.2.3 on 2023-07-31 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0006_practiceavailable_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practiceavailable',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
