# Generated by Django 4.2.3 on 2023-07-31 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0007_alter_practiceavailable_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='practiceavailable',
            name='title',
            field=models.TextField(default=''),
        ),
    ]
