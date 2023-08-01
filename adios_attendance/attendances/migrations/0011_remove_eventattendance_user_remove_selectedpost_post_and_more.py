# Generated by Django 4.2.3 on 2023-07-31 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0010_practicedate_practicedatedetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventattendance',
            name='user',
        ),
        migrations.RemoveField(
            model_name='selectedpost',
            name='post',
        ),
        migrations.RemoveField(
            model_name='selectedpost',
            name='user',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='available_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendances.practicedate'),
        ),
        migrations.DeleteModel(
            name='AvailableDate',
        ),
        migrations.DeleteModel(
            name='EventAttendance',
        ),
        migrations.DeleteModel(
            name='SelectedPost',
        ),
    ]
