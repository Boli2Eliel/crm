from django.contrib.auth.models import User
from django.db import models
from team.models import Team

# Create your models here.
class Client(models.Model):
    #team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE, verbose_name='Equipe')
    firm = models.CharField(max_length=20, verbose_name="Raison sociale (personne morale)")
    first_name = models.CharField(max_length=20, verbose_name="Prénom")
    name = models.CharField(max_length=150, verbose_name='Nom')
    email = models.EmailField(verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="Téléphone")
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    converted_date = models.DateTimeField(null=True, blank=True, verbose_name="Date_conversion_en_client")
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/",
                                        verbose_name="Photo de profil")
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE, verbose_name='Créé par')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta :
        ordering = ('-modified_at',)

    def __str__(self):
        return self.name

    def get_team_name(self):
        return self.team.name

class ClientFile(models.Model):
    team = models.ForeignKey(Team, related_name='client_files', on_delete=models.CASCADE, verbose_name='Equipe')
    client = models.ForeignKey(Client, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='clientfiles', verbose_name='Fichier')
    created_by = models.ForeignKey(User, related_name='client_files', on_delete=models.CASCADE, verbose_name='Créé par')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username

class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='client_comments', on_delete=models.CASCADE, verbose_name='Equipe')
    client = models.ForeignKey(Client, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True, verbose_name='Contenu')
    created_by = models.ForeignKey(User, related_name='client_comments', on_delete=models.CASCADE, verbose_name='Créé par')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username

