# Generated by Django 3.2.7 on 2022-07-20 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0003_auto_20220720_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ex_user',
            old_name='name',
            new_name='firstname',
        ),
        migrations.AddField(
            model_name='ex_user',
            name='lastname',
            field=models.CharField(default='default', max_length=50),
        ),
    ]
