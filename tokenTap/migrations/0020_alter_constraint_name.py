# Generated by Django 4.0.4 on 2023-10-27 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokenTap', '0019_alter_constraint_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constraint',
            name='name',
            field=models.CharField(choices=[('BrightIDMeetVerification', 'BrightIDMeetVerification'), ('BrightIDAuraVerification', 'BrightIDAuraVerification'), ('OncePerMonthVerification', 'OncePerMonthVerification'), ('OnceInALifeTimeVerification', 'OnceInALifeTimeVerification'), ('OptimismHasClaimedGasInThisRound', 'OptimismHasClaimedGasInThisRound')], max_length=255, unique=True),
        ),
    ]
