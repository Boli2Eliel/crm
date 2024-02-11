# Generated by Django 4.2.1 on 2023-07-27 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_plan'),
        ('lead', '0003_lead_team'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lead',
            options={'ordering': ('-modified_at',)},
        ),
        migrations.AlterField(
            model_name='lead',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='team.team', verbose_name='Equipe'),
        ),
    ]