# Generated by Django 4.0.4 on 2022-06-07 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faucet', '0014_walletaccount_remove_chain_wallet_key_chain_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='chain',
            name='fund_manager_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
