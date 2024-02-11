from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom')
    price = models.IntegerField(verbose_name='Prix')
    description = models.TextField(blank=True, null=True)
    max_leads =models.IntegerField()
    max_clients =models.IntegerField()

    def __str__(self):
        return self.name

class Team(models.Model):
    #plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="teams")
    name = models.CharField(max_length=150, verbose_name='Nom')
    members = models.ManyToManyField(User, related_name='teams', verbose_name='Membre')
    created_by = models.ForeignKey(User, related_name='create_teams', on_delete=models.CASCADE, verbose_name='créé par')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')

    def __str__(self):
        return self.name

