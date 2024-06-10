# Generated by Django 5.0.4 on 2024-04-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=70)),
                ('title', models.CharField(default='', max_length=70)),
                ('content', models.CharField(default='', max_length=70)),
                ('slug', models.CharField(default='', max_length=300)),
                ('date', models.DateTimeField(blank=True)),
            ],
        ),
    ]