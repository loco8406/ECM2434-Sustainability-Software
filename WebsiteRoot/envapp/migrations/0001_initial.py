# Generated by Django 5.1.6 on 2025-02-06 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testfield', models.CharField(max_length=200)),
                ('testdate', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
