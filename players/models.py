from django.db import models

class Player(models.Model):
    class Position(models.TextChoices):
        GOALKEEPER = 'G'
        DEFENDER = 'D'
        MIDFIELDER = 'M'
        FORWARD = 'F'

    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    position = models.CharField(
        max_length=1, choices=Position
    )
    birth_date = models.DateField()
    market_value = models.DecimalField(max_digits=9, decimal_places=2)
    photo = models.ImageField(
        upload_to='players/photos/', default='players/photos/default.png', blank=True, null=True
    )
    team = models.ForeignKey(
        'teams.Team', related_name='players', on_delete=models.CASCADE
    )