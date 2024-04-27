from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegisterForm


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "registration/signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verificar si el usuario existe en la base de datos y si está activo
        user = User.objects.filter(username=username, is_active=True).first()
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