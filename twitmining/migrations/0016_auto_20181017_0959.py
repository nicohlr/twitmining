# Generated by Django 2.1.2 on 2018-10-17 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitmining', '0015_relevanttweet_score'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tweet',
        ),
        migrations.RemoveField(
            model_name='relevanttweet',
            name='score',
        ),
    ]
