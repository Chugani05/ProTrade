from django.db import models

class Team(models.Model):
    class League(models.TextChoices):
        LALIGA = 'L'
        PREMIER = 'P'
        CALCIO = 'C'
        BUNDESLIGA = 'B'
    
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    league = models.CharField(
        max_length=1, choices=League
    )
    shield = models.ImageField(
        upload_to='teams/shields/', default='teams/shields/default.png', blank=True, null=True
    )