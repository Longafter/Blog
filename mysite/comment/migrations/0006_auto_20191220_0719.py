# Generated by Django 2.1.8 on 2019-12-19 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_auto_20191220_0231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_time']},
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]