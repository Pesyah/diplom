# Generated by Django 4.2.1 on 2023-05-31 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('optics', '0002_optics_delete_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optics',
            name='picture',
            field=models.ImageField(upload_to=''),
        ),
    ]
