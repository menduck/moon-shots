# Generated by Django 3.2.18 on 2023-05-23 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='playlist',
            new_name='playlists',
        ),
        migrations.AddField(
            model_name='playlist',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='musics.room'),
        ),
    ]
