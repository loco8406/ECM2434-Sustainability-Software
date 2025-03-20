<<<<<<< Updated upstream
<<<<<<< Updated upstream
# Generated by Django 5.1.6 on 2025-03-19 18:07
=======
# Generated by Django 5.1.6 on 2025-03-19 14:39
>>>>>>> Stashed changes
=======
# Generated by Django 5.1.6 on 2025-03-19 14:39
>>>>>>> Stashed changes

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
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
        migrations.CreateModel(
            name='StationUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField()),
                ('waterStationID', models.IntegerField()),
                ('fillTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-fillTime'],
            },
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoTitle', models.CharField(max_length=200)),
                ('videoThumbnailURL', models.CharField(max_length=200)),
                ('videoLink', models.CharField(max_length=200)),
                ('videoPoints', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VideoWatchers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField()),
                ('videoID', models.IntegerField()),
                ('watchTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaterStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('location_description', models.TextField()),
                ('points_reward', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(default='user', max_length=30)),
                ('points', models.IntegerField(default=0)),
                ('referral_code', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('consent_timestamp', models.DateTimeField(auto_now_add=True)),
                ('fuelRemaining', models.IntegerField(default=0)),
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                ('bottle_size', models.CharField(choices=[('500ml', '500ml'), ('750ml', '750ml'), ('1000ml', '1L'), ('1500ml', '1.5L'), ('2000ml', '2L')], default='750ml', max_length=10)),
=======
                ('bottle_size', models.CharField(choices=[('500ml', '500ml'), ('750ml', '750ml'), ('1000ml', '1L'), ('1500ml', '1.5L'), ('2000ml', '2L')], default='500ml', max_length=10)),
>>>>>>> Stashed changes
=======
                ('bottle_size', models.CharField(choices=[('500ml', '500ml'), ('750ml', '750ml'), ('1000ml', '1L'), ('1500ml', '1.5L'), ('2000ml', '2L')], default='500ml', max_length=10)),
>>>>>>> Stashed changes
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
