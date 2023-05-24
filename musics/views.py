from django.shortcuts import render, redirect
from .models import Room, Playlist
from .forms import RoomForm

# Create your views here.
def index(request):
    rooms = Room.objects.order_by('-pk')
    return render(request, 'musics/index.html', {'rooms':rooms})


def create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('musics:index')
    else:
        form = RoomForm

    return render(request, 'musics/create.html', {'form':form})