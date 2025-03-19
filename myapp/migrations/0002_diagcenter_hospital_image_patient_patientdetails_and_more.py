# Generated by Django 4.2 on 2024-02-14 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dcid', models.CharField(max_length=50)),
                ('dcname', models.CharField(max_length=500)),
                ('pincode', models.CharField(max_length=6)),
                ('state', models.CharField(max_length=50)),
                ('dist', models.CharField(max_length=60)),
                ('Address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hid', models.CharField(max_length=50)),
                ('hname', models.CharField(max_length=500)),
                ('pincode', models.CharField(max_length=6)),
                ('state', models.CharField(max_length=50)),
                ('dist', models.CharField(max_length=60)),
                ('Address', models.CharField(max_length=100)),
                ('speciality', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
                ('hid', models.CharField(max_length=50)),
                ('hname', models.CharField(max_length=50)),
                ('img', models.ImageField(blank=True, upload_to='images/')),
                ('adhno', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adhno', models.CharField(max_length=12)),
                ('pname', models.CharField(max_length=500)),
                ('pincode', models.CharField(max_length=6)),
                ('state', models.CharField(max_length=50)),
                ('dist', models.CharField(max_length=60)),
                ('Address', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=20)),
                ('dob', models.CharField(max_length=15)),
                ('diab', models.CharField(max_length=10)),
                ('bp', models.CharField(max_length=10)),
                ('weight', models.CharField(max_length=10)),
                ('height', models.CharField(max_length=10)),
                ('phno', models.CharField(max_length=20)),
                ('emial', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PatientDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
                ('disease', models.CharField(max_length=400)),
                ('diagnosis', models.CharField(max_length=500)),
                ('prescription', models.CharField(max_length=1000)),
                ('remarks', models.CharField(max_length=500)),
                ('adhno', models.CharField(max_length=12)),
                ('hid', models.CharField(max_length=50)),
                ('hname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='pdfs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
                ('hid', models.CharField(max_length=50)),
                ('hname', models.CharField(max_length=50)),
                ('pdf', models.FileField(blank=True, upload_to='pdfs/')),
                ('adhno', models.CharField(max_length=12)),
            ],
        ),
    ]
