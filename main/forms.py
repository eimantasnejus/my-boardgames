from django import forms
from main.models import Playthrough


class PlaythroughForm(forms.ModelForm):
    class Meta:
        model = Playthrough
        fields = ['boardgame', 'datetime', 'players', 'playtime']
