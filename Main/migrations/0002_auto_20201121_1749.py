# Generated by Django 3.1.2 on 2020-11-21 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='category',
            field=models.ForeignKey(db_column='title', null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.category'),
        ),
    ]