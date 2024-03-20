import os
from datetime import datetime, timedelta
from github import Github

# Token de acceso personal de GitHub
github_token = os.getenv('TOKEN')

# Nombre de usuario y nombre del repositorio
username = 'Troter2'
repository_name = 'HotelManagementProject'

# Crear una instancia de la clase Github
g = Github(github_token)

# Obtener el repositorio
repo = g.get_user(username).get_repo(repository_name)

print(repo)
