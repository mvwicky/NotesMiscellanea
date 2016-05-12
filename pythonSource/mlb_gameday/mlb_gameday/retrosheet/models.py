from django.db import models

# Create your models here.


class Team(models.Model):
    year = models.SmallIntegerField()
    abbreviation = models.CharField(max_length=10)
    league = models.CharField(max_length=2)
    city = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return str('{}, {}, {}, {}, {}'
                   .format(year, abbreviation, league, city, name))
