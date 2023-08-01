# Generated by Django 4.2.3 on 2023-07-31 23:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0011_remove_eventattendance_user_remove_selectedpost_post_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('content', models.TextField(default='')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('attendees', models.ManyToManyField(through='attendances.Attendance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='available_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendances.availabledate'),
        ),
    ]
