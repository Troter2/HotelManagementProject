from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from accounts.models import CustomUser
from .forms import RegisterForm


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        username = response.POST.get('username')
        password = response.POST.get('password1')
        user = CustomUser.objects.filter(username=username, is_active=True).first()
        if user is not None:
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(response, authenticated_user)
                return redirect("/home")
        return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "registration/signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verificar si el usuario existe en la base de datos y si está activo
        user = CustomUser.objects.filter(username=username, is_active=True).first()
        if user is not None:
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect("/home")
        # Si el usuario no es válido, mostrar mensaje de error
        error_message = "Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo."
        return render(request, "registration/login.html", {"error_message": error_message})
    else:
        return render(request, "registration/login.html")
