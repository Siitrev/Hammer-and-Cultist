# Generated by Django 4.2.5 on 2024-02-03 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_tag_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default=None, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
