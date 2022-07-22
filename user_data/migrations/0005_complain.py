# Generated by Django 3.2.7 on 2022-07-22 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_data', '0004_auto_20220720_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complain_name', models.CharField(default='default', max_length=50)),
                ('complain_type', models.CharField(default='default', max_length=15)),
                ('complain_description', models.CharField(default='default', max_length=150)),
                ('complain_date', models.DateField()),
                ('complain_status', models.BooleanField(default=False)),
                ('complain_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
