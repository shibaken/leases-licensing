# Generated by Django 3.2.13 on 2022-08-26 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0077_competitiveprocess_generated_proposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitiveprocess',
            name='generated_proposal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='originating_competitive_process', to='leaseslicensing.proposal'),
        ),
    ]