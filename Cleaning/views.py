from django.shortcuts import render
from Cleaning.models import


# Create your views here.

def CleanerPage(request):
    rooms = Cleaning.objects.all()
    return render(request, 'Cleaner/cleaner_page.html')
