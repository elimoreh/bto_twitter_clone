# Generated by Django 4.1.7 on 2023-03-06 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]