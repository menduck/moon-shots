from django import forms
from .models import Room, Playlist

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('title', 'content',)