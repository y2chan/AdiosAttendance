# Generated by Django 4.2.3 on 2023-08-01 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0014_alter_practicedatedetail_practice_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practicedatedetail',
            name='is_attending',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
