# Generated by Django 3.2.12 on 2022-02-24 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leaseslicensing", "0039_proposal_shapefile_json"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approval",
            name="proxy_applicant",
            field=models.IntegerField(null=True),
        ),
    ]
