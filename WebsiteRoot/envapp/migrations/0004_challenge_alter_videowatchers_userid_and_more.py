# Generated by Django 5.1.6 on 2025-02-08 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('envapp', '0003_videos_videowatchers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.TextField()),
                ('challenge_date', models.DateTimeField()),
                ('points_reward', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='videowatchers',
            name='userID',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='videowatchers',
            name='videoID',
            field=models.IntegerField(),
        ),
    ]
