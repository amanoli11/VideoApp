# Generated by Django 4.0.6 on 2022-07-20 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VideoApp', '0004_alter_video_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_size',
            field=models.TextField(editable=False, null=True),
        ),
    ]
