# Generated by Django 4.0.4 on 2023-10-24 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faucet', '0062_rename_tokentap_weekly_claim_limit_globalsettings_tokentap_round_claim_limit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='globalsettings',
            old_name='prizetap_weekly_claim_limit',
            new_name='prizetap_round_claim_limit',
        ),
    ]
