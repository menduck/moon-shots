from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Create your views here.
def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    context = {
        'room_name_json': mark_safe(json.dumps(room_name))
    }
    print(1, context)
    return render(request, 'chat/room.html', context)