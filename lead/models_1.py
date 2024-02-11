from django.contrib.auth.models import User
from django.db import models

from team.models import Team

class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

# Create your models here.
class Lead(models.Model):
    LOW = 'basse'
    MEDIUM = 'medium'
    HIGH = 'haute'

    CHOICES_PRIORITY = (
        (LOW, 'Basse'),
        (MEDIUM, 'Medium'),
        (HIGH, 'Haute'),
    )

    NEW = 'nouveau'
    CONTACTED ='contacté'
    WON = 'gagné'
    LOST = 'lost'

    CHOICES_STATUS = (
        (NEW, 'Nouveau'),
        (CONTACTED, 'Contacté'),
        (WON, 'Gagné'),
        (LOST, 'Perdu'),
    )

    team = models.ForeignKey(Team, related_name='leads', on_delete=models.CASCADE, verbose_name='Equipe' )
    first_name = models.CharField(max_length=20, verbose_name="Prénom")
    last_name = models.CharField(max_length=150, verbose_name='Nom')
    email = models. EmailField()
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    priority = models.CharField(max_length=15, choices=CHOICES_PRIORITY, default=MEDIUM, verbose_name='Priorité')
    status = models.CharField(max_length=15, choices=CHOICES_STATUS, default=NEW, verbose_name='Etat')
    converted_to_client = models.BooleanField(default=False, verbose_name="Convertir en client")
    converted_date = models.DateTimeField(null=True, blank=True, verbose_name="Date_conversion_en_client")
    phone_number = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/",
                                        verbose_name="Photo de profil")
    created_by = models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE, verbose_name='Créé par')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = LeadManager()

    class Meta :
        ordering = ('-modified_at',)

    def __str__(self):
        return self.name

class LeadFile(models.Model):
    team = models.ForeignKey(Team, related_name='lead_files', on_delete=models.CASCADE, verbose_name='Equipe')
    lead = models.ForeignKey(Lead, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='leadfiles', verbose_name='Fichier')
    created_by = models.ForeignKey(User, related_name='lead_files', on_delete=models.CASCADE, verbose_name='Créé par')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username

class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='lead_comments', on_delete=models.CASCADE, verbose_name='Equipe')
    lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True, verbose_name='Contenu')
    created_by = models.ForeignKey(User, related_name='lead_comments', on_delete=models.CASCADE, verbose_name='Créé par')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username