const axios = require('axios');

// Configurar variables de entorno
const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

// Función para crear un nuevo ítem en la base de datos de Notion
async function createNotionTask(issueTitle, issueUrl) {
  const notionUrl = `https://api.notion.com/v1/pages`;
  
  // Configuración del cuerpo de la solicitud a la API de Notion
  const data = {
    parent: { database_id: databaseId },
    properties: {
      Title: {
        title: [
          {
            text: {
              content: issueTitle,
            },
          },
        ],
      },
      URL: {
        url: issueUrl,
      },
    },
  };

  try {
    const response = await axios.post(notionUrl, data, {
      headers: {
        'Authorization': `Bearer ${notionApiKey}`,
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
      },
    });
    console.log('Task created in Notion:', response.data);
  } catch (error) {
    console.error('Error creating task in Notion:', error.response ? error.response.data : error.message);
  }
}

// Obtener datos del issue del contexto de GitHub Actions
const issueTitle = process.env.GITHUB_EVENT_ISSUE_TITLE || 'No title';
const issueUrl = process.env.GITHUB_EVENT_ISSUE_URL || '';

createNotionTask(issueTitle, issueUrl);
