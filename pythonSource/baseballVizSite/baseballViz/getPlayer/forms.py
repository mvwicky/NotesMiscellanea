from django import forms 
from django.utils import timezone

class PlayerForm(forms.Form):
	player_name = forms.CharField(label='Player Name', max_length=200, strip=True)
	batted_ball = forms.BooleanField(label='Batted Ball Map', required=False)
	zone_map = forms.BooleanField(label='Strike Zone Heat Map', required=False)
	year = forms.TypedChoiceField(label='Year',
								  choices=[(str(x), str(x)) for x in range(2008, timezone.now().year + 1)], 
								  coerce=int, 
								  empty_value=None)