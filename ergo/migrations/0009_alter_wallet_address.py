# Generated by Django 3.2.5 on 2021-10-09 00:59

from django.db import migrations, models
import ergo.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ergo', '0008_alter_wallet_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='address',
            field=models.CharField(max_length=300, validators=[ergo.validators.validate_address]),
        ),
    ]
