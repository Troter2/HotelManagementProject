const { Octokit } = require("@octokit/core");

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

async function updateChecklist() {
  try {
    const issues = await octokit.request('GET /repos/{owner}/{repo}/issues', {
      owner: 'tu-usuario',
      repo: 'tu-repositorio'
    });

    // Lógica para contar el número de issues abiertas y cerradas en la semana
    let openedThisWeek = 0;
    let closedThisWeek = 0;
    const currentDate = new Date();
    const oneWeekAgo = new Date(currentDate.getTime() - 7 * 24 * 60 * 60 * 1000);

    issues.data.forEach(issue => {
      const createdAt = new Date(issue.created_at);
      const closedAt = issue.closed_at ? new Date(issue.closed_at) : null;

      if (createdAt >= oneWeekAgo) {
        openedThisWeek++;
      }

      if (closedAt && closedAt >= oneWeekAgo) {
        closedThisWeek++;
      }
    });

    // Lógica para actualizar la checklist en algún archivo markdown dentro del repositorio
    // Por ejemplo, podrías actualizar un archivo llamado CHECKLIST.md
    const checklistContent = `
- Issues Abiertas Esta Semana: ${openedThisWeek}
- Issues Cerradas Esta Semana: ${closedThisWeek}
`;

    await octokit.request('PUT /repos/{owner}/{repo}/contents/{path}', {
      owner: 'tu-usuario',
      repo: 'tu-repositorio',
      path: 'CHECKLIST.md',
      message: 'Actualizar Checklist',
      content: Buffer.from(checklistContent).toString('base64'),
      sha: 'SHA del archivo CHECKLIST.md actual'
    });

    console.log('Checklist actualizado con éxito.');
  } catch (error) {
    console.error('Error al actualizar el checklist:', error);
  }
}

updateChecklist();
