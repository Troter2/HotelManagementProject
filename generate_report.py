import os
from datetime import datetime, timedelta
from github import Github

# Token de acceso personal de GitHub
github_token = os.getenv('GITHUB_TOKEN')

# Nombre de usuario y nombre del repositorio
repository_name = 'HotelManagementProject'

# Crear una instancia de la clase Github
g = Github(github_token)

# Obtener el repositorio
repo = g.get_repo(repository_name)

print(repo)
