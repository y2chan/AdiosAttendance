# Generated by Django 4.2.3 on 2023-08-02 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0017_vote_votechoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votechoice',
            name='vote',
        ),
        migrations.RemoveField(
            model_name='votechoice',
            name='voters',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
        migrations.DeleteModel(
            name='VoteChoice',
        ),
    ]
