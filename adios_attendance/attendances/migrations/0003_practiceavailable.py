# Generated by Django 4.2.3 on 2023-07-31 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0002_notice'),
    ]

    operations = [
        migrations.CreateModel(
            name='PracticeAvailable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
