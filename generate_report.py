import os
import pandas as pd
from datetime import datetime, timedelta
from github import Github
import matplotlib.pyplot as plt

def generate_weekly_report(github_token, username, repository_name):
    # Crear una instancia de la clase Github
    g = Github(github_token)

    # Obtener el repositorio
    repo = g.get_repo(f"{username}/{repository_name}")

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
    
    def get_day_of_week(date_str):
        date = datetime.strptime(date_str[:10], '%Y-%m-%d')
        return date.strftime('%A')
    
    current_date = datetime.now()
    one_week_ago = current_date - timedelta(days=7)
    
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
                
    # Extraer los datos para la tabla
    dias = list(weekly_counts.keys())
    abiertas = [weekly_counts[d]["opened"] for d in weekly_counts]
    cerradas = [weekly_counts[d]["closed"] for d in weekly_counts]

    data = {
        "Día de la Semana": dias,
        "Abiertas": abiertas,
        "Cerradas": cerradas
    }
    # Crear la tabla
    df = pd.DataFrame()
    
    # Crear figura y eje
    fig, ax = plt.subplots()
    
    # Eliminar marcas del eje
    ax.axis('off')
    
    # Crear tabla
    tabla = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     cellLoc='center',
                     loc='center')

    # Ajustar tamaño de la fuente
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)

    # Ajustar tamaño de la tabla
    tabla.scale(1.5, 1.5)

    # Guardar la imagen como PNG
    plt.savefig('tabla_semanal.png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.show()

    # Calcular la semana actual
    current_date = datetime.now()
    one_week_ago = current_date - timedelta(days=7)

    # Recorrer todas las issues y contar las abiertas y cerradas por día de la semana
    """

    # Imprimir la tabla
    print('Día de la Semana | Abiertas | Cerradas')
    print('----------------------------------------')
    total_closed = 0
    total_opened = 0
    for day, counts in weekly_counts.items():
        print(f'{day.ljust(16)}| {str(counts["opened"]).rjust(8)} | {str(counts["closed"]).rjust(8)}')
        total_opened += counts["opened"]
        total_closed += counts["closed"]
        
    print(f'{("Total").ljust(16)}| {str(total_opened).rjust(8)} | {str(total_closed).rjust(8)}')
    print('----------------------------------------')
    """
    
# Obtener el token de acceso personal de GitHub de los secrets
github_token = os.getenv('GITHUB_TOKEN')

# Nombre de usuario y nombre del repositorio
username = 'Troter2'
repository_name = 'HotelManagementProject'

# Generar el informe semanal
generate_weekly_report(github_token, username, repository_name)
