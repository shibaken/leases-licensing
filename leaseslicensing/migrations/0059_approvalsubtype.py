# Generated by Django 3.2.13 on 2022-08-12 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0058_merge_20220810_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalSubType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]