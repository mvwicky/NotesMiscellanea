import datetime

from django import forms 
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect , Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Player, Year
from .forms import PlayerForm
# Create your views here.

def index(request):
	if request.method == 'POST':
		form = PlayerForm(request.POST)
		print(form)
		print(form.data)
		if form.is_valid():
			print(form.cleaned_data)
			name = form.cleaned_data['player_name']
			year = form.cleaned_data['year']
			batted_ball = form.cleaned_data['batted_ball']
			zone_map = form.cleaned_data['zone_map']
			if not batted_ball and not zone_map:
				error_message = "You Must Select An Option"
			else:
				print(name)
				print(year)
				player = Player(player_text=name, player_id_num=year, last_queried=timezone.now())
				player.save()
				error_message = None
		else:
			print(form.errors)
			print(form.cleaned_data)
			error_message = "Invalid Inputs"
	else:
		error_message = None
	latest_player_list = Player.objects.order_by('-last_queried')[:10]
	form = PlayerForm()
	context = {'latest_player_list': latest_player_list, 
				   'form': form,
				   'error_message': error_message}

	return render(request, 'getPlayer/index.html', context)


# 			# Check if player name exists in gameday files
# 			# Get id number from gameday files
# 			id_num = 0

# 			# Check if player has db entry 
# 			if not Player.objects.filter(player_name=name, player_id_num=id_num):
# 				player = None # create db entry for player

# 			# Check if player has db entry for year 
# 			if not Year.objects.filter(player_name=name, player_id_num=id_num):
# 				year = None # create db entry for player year

# 			if batted_ball:
# 				if not year.batted_ball_exists:
# 					pass # create image and send it to the results page
				

# 			if zone_map:
# 				if not year.zone_map_exists:
# 					pass # create image and send it to the results page

# 			player.last_queried = timezone.now() 
# 			return HttpResponseRedirect(reverse('getPlayer:results', args=(player.id, )))

def get_options(request):
	return index(request)

class DetailView(generic.DetailView):
	model = Player
	template_name = 'getPlayer/detail.html'

class ResultsView(generic.DetailView):
	model = Player 
	template_name = 'getPlayer/results.html'

