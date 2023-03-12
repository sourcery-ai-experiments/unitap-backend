# Generated by Django 4.0.4 on 2023-03-08 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0008_alter_userprofile_user_alter_wallet_user_profile"),
        ("faucet", "0031_chain_is_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="claimreceipt",
            name="bright_user",
        ),
        migrations.AddField(
            model_name="claimreceipt",
            name="user_profile",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="claims",
                to="authentication.userprofile",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="chain",
            name="chain_type",
            field=models.CharField(
                choices=[("EVM", "EVM"), ("NONEVM", "Non-EVM")],
                default="EVM",
                max_length=10,
            ),
        ),
    ]
