from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                # Personaliza el mensaje de error aquí
                error_message = "Nombre de usuario o contraseña incorrectos. Por favor, vuelvelo a intentar."
                print(error_message)
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
