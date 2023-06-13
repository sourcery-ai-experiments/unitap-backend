# Generated by Django 4.0.4 on 2023-06-10 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faucet', '0047_globalsettings_is_gas_tap_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='prizetap_weekly_claim_limit',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='globalsettings',
            name='tokentap_weekly_claim_limit',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='globalsettings',
            name='weekly_chain_claim_limit',
            field=models.IntegerField(default=5),
        ),
    ]
