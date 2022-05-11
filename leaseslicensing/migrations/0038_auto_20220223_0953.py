# Generated by Django 3.2.12 on 2022-02-23 01:53

from django.db import migrations, models
import django.db.models.deletion
import leaseslicensing.components.proposals.models


class Migration(migrations.Migration):

    dependencies = [
        ("leaseslicensing", "0037_proposalmapdocument"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShapefileDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=500,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shapefile_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="ProposalMapDocument",
        ),
    ]
