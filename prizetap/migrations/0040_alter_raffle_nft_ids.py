# Generated by Django 4.0.4 on 2023-11-09 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prizetap', '0039_rename_nft_id_raffle_nft_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raffle',
            name='nft_ids',
            field=models.TextField(blank=True, null=True),
        ),
    ]
