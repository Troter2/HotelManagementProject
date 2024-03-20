const { Octokit } = require("@octokit/core");

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

async function generateWeeklyReport() {
  try {
    const issues = await octokit.request('GET /repos/{owner}/{repo}/issues', {
      owner: 'Troter2',
      repo: 'HotelManagementProject'
    });

    // Objeto para almacenar el recuento de issues por día de la semana
    const weeklyCounts = {
      'Monday': { opened: 0, closed: 0 },
      'Tuesday': { opened: 0, closed: 0 },
      'Wednesday': { opened: 0, closed: 0 },
      'Thursday': { opened: 0, closed: 0 },
      'Friday': { opened: 0, closed: 0 },
      'Saturday': { opened: 0, closed: 0 },
      'Sunday': { opened: 0, closed: 0 }
    };

    // Función para obtener el nombre del día de la semana
    function getDayOfWeek(dateString) {
      const date = new Date(dateString);
      const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      return daysOfWeek[date.getDay()];
    }

    // Recorre todas las issues y cuenta las abiertas y cerradas por día de la semana
    issues.data.forEach(issue => {
      const dayOfWeek = getDayOfWeek(issue.created_at);
      const closedAt = issue.closed_at ? getDayOfWeek(issue.closed_at) : null;

      // Aumenta el contador de issues abiertas para el día correspondiente
      weeklyCounts[dayOfWeek].opened++;

      // Si la issue está cerrada, aumenta el contador de issues cerradas para el día correspondiente
      if (closedAt) {
        weeklyCounts[closedAt].closed++;
      }
    });

    // Genera la tabla gráfica
    console.log('Día de la Semana | Abiertas | Cerradas');
    console.log('----------------------------------------');
    for (const day in weeklyCounts) {
      console.log(`${day.padEnd(16)}| ${weeklyCounts[day].opened.toString().padStart(8)} | ${weeklyCounts[day].closed.toString().padStart(8)}`);
    }
  } catch (error) {
    console.error('Error al generar el informe semanal:', error);
  }
}

generateWeeklyReport();
