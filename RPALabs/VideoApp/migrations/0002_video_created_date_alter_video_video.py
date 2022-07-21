# Generated by Django 4.0.6 on 2022-07-20 19:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('VideoApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(blank=True, upload_to='videos/'),
        ),
    ]
