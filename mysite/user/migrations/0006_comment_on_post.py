# Generated by Django 4.2.5 on 2023-11-09 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_image'),
        ('user', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='on_post',
            field=models.ManyToManyField(to='blog.post'),
        ),
    ]
