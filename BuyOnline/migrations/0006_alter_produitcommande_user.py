# Generated by Django 4.1 on 2022-08-09 12:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BuyOnline', '0005_produitcommande_ordered_produitcommande_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produitcommande',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]