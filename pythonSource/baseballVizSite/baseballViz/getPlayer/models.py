import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Player(models.Model):
	player_text = models.CharField('Player Name',max_length=200)
	player_id_num = models.PositiveIntegerField('Player ID', default=1)
	last_queried = models.DateTimeField(default=datetime.datetime.now())
	last_year_queried = models.PositiveSmallIntegerField(default=datetime.datetime.now().year)
	def __str__(self):
		return self.player_text

class Year(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	year_value = models.PositiveSmallIntegerField('Year', default=datetime.datetime.now().year)
	batted_ball_exists = models.BooleanField(default=False)
	zone_map_exists = models.BooleanField(default=False)
	batted_ball_img = models.ImageField()
	zone_map_img = models.ImageField()


class Team(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE)
	team_name = models.CharField('Team Name', max_length=200) 
	league = models.CharField('Team Name', max_length=50)

