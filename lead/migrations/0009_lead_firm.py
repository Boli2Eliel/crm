# Generated by Django 4.2.1 on 2023-08-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0008_lead_converted_date_lead_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='firm',
            field=models.CharField(default=1, max_length=20, verbose_name='Raison sociale (personne morale'),
            preserve_default=False,
        ),
    ]