# Generated by Django 4.2.1 on 2023-07-25 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField(blank=True, null=True)),
                ('priority', models.CharField(choices=[('basse', 'basse'), ('medium', 'Medium'), ('haute', 'Haute')], default='medium', max_length=15)),
                ('status', models.CharField(choices=[('nouveau', 'Nouveau'), ('contacté', 'Contacté'), ('gagné', 'Gagné'), ('lost', 'Perdu')], default='nouveau', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
