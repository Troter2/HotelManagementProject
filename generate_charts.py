import matplotlib.pyplot as plt
import datetime

# Fechas de inicio y finalización del sprint
fecha_inicio = datetime.date(2024, 4, 5)
fecha_fin = datetime.date(2024, 5, 2)

# Número de días del sprint
dias_sprint = (fecha_fin - fecha_inicio).days

# Datos de ejemplo para las issues cerradas por día (puedes obtener estos datos de tu sistema de seguimiento de problemas)
# Aquí se muestran los datos proporcionados
issues_cerradas_por_dia = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,1, 2, 0, 0, 6, 0, 0, 0, 0, 1, 1, 0, 0, 4, 14, 33]

# Fechas para el eje x (por ejemplo, el período del sprint)
fechas = [fecha_inicio + datetime.timedelta(days=i) for i in range(dias_sprint)]

# Calcular la línea de tendencia de burn-down (ideal) y burn-up (real)
linea_burn_down_ideal = [max(20 - i, 0) for i in range(dias_sprint)]
linea_burn_down_real = [max(20 - sum(issues_cerradas_por_dia[:i+1]), 0) for i in range(dias_sprint)]
linea_burn_up = [sum(issues_cerradas_por_dia[:i+1]) for i in range(dias_sprint)]

# Graficar burn-down chart
plt.figure(figsize=(10, 6))
plt.plot(fechas, linea_burn_down_ideal, linestyle='--', color='red', label='Línea de tendencia de burn-down (ideal)')
plt.plot(fechas, linea_burn_down_real, linestyle='-', color='green', label='Línea de tendencia de burn-down (real)')
plt.plot(fechas, issues_cerradas_por_dia, marker='o', label='Issues cerradas', color='blue')  # Línea para las issues cerradas
plt.fill_between(fechas, linea_burn_down_ideal, color='red', alpha=0.1)  # Relleno para el área bajo la línea de tendencia de burn-down (ideal)
plt.xlabel('Fecha')
plt.ylabel('Cantidad de issues')
plt.title('Gráfico de burn-down')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('burn_down_chart.png')

# Graficar burn-up chart
plt.figure(figsize=(10, 6))
plt.plot(fechas, linea_burn_up, marker='o', label='Progreso real (burn-up)')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de issues')
plt.title('Gráfico de burn-up')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('burn_up_chart.png')
