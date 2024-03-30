from django.shortcuts import render
from User.models import Shift


# Create your views here.

def shift_management_page(request):
    users = Shift.objects.all()
    return render(request, 'personal_manager/shift_management_page.html', {'users': users})
