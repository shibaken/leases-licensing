# Generated by Django 3.2.13 on 2022-10-26 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0117_merge_0116_auto_20221011_1144_0116_auto_20221021_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalassessment',
            name='referral',
        ),
        migrations.AddField(
            model_name='proposal',
            name='assessor_comment_proposal_details',
            field=models.TextField(blank=True),
        ),
    ]