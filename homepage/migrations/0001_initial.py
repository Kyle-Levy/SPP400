# Generated by Django 2.1.5 on 2019-02-09 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('password', models.CharField(max_length=1000)),
                ('email', models.CharField(max_length=1000)),
                ('phone', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('uuid', models.IntegerField()),
            ],
        ),
    ]
