import os
from datetime import datetime, timedelta
from github import Github

# Token de acceso personal de GitHub
github_token = os.getenv('GITHUB_TOKEN')

# Nombre de usuario y nombre del repositorio
username = 'tu-usuario'
repository_name = 'tu-repositorio'

# Crear una instancia de la clase Github
g = Github(github_token)

# Obtener el repositorio
repo = g.get_user(username).get_repo(repository_name)

# Obtener todas las issues del repositorio
issues = repo.get_issues(state='all')

# Diccionario para almacenar el recuento de issues por día de la semana
weekly_counts = {
    'Monday': {'opened': 0, 'closed': 0},
    'Tuesday': {'opened': 0, 'closed': 0},
    'Wednesday': {'opened': 0, 'closed': 0},
    'Thursday': {'opened': 0, 'closed': 0},
    'Friday': {'opened': 0, 'closed': 0},
    'Saturday': {'opened': 0, 'closed': 0},
    'Sunday': {'opened': 0, 'closed': 0}
}

# Función para obtener el día de la semana
def get_day_of_week(date_str):
    date = datetime.strptime(date_str[:10], '%Y-%m-%d')
    return date.strftime('%A')

# Calcular la semana actual
current_date = datetime.now()
one_week_ago = current_date - timedelta(days=7)

# Recorrer todas las issues y contar las abiertas y cerradas por día de la semana
for issue in issues:
    created_at = issue.created_at.replace(tzinfo=None)
    if created_at >= one_week_ago:
        day_of_week = get_day_of_week(str(created_at))
        weekly_counts[day_of_week]['opened'] += 1

    if issue.closed_at:
        closed_at = issue.closed_at.replace(tzinfo=None)
        if closed_at >= one_week_ago:
            day_of_week = get_day_of_week(str(closed_at))
            weekly_counts[day_of_week]['closed'] += 1

# Imprimir la tabla
print('Día de la Semana | Abiertas | Cerradas')
print('----------------------------------------')
for day, counts in weekly_counts.items():
    print(f'{day.ljust(16)}| {str(counts["opened"]).rjust(8)} | {str(counts["closed"]).rjust(8)}')

