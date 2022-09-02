# Generated by Django 3.2.13 on 2022-09-02 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0081_auto_20220826_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryDocumentCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('_file', models.FileField(max_length=255, upload_to='')),
                ('temp_document_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='leaseslicensing.temporarydocumentcollection')),
            ],
        ),
    ]