# Generated by Django 3.0.5 on 2022-11-13 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedDonors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('city', models.CharField(blank=True, max_length=300)),
                ('blood_group', models.CharField(max_length=5)),
            ],
        ),
    ]
