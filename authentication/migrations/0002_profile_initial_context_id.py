# Generated by Django 4.0.4 on 2023-02-26 18:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='initial_context_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
