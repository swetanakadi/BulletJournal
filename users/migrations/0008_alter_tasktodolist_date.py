# Generated by Django 4.0.3 on 2022-06-28 06:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_taskchecklist_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktodolist',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]