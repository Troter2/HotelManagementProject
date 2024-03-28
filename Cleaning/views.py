from django.shortcuts import render
from Reception.models import Room


# Create your views here.

def cleaner_page(request):
    rooms = Room.objects.all()
    return render(request, 'Cleaner/cleaner_page.html', {'rooms': rooms})
