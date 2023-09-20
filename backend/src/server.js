const express = require('express');
const app = express();
const path = require('path');
const fs = require('fs');

const PORT = 3000; // Pode ser qualquer porta disponível

// Define o diretório de onde os arquivos estáticos (como o HTML) serão servidos
app.use(express.static(path.join(__dirname, '/Users/gusta/dev/iqOptionBotTrader/public')));

// Rota para retornar os dados do arquivo JSON
app.get('/dados', (req, res) => {
    fs.readFile('/Users/gusta/dev/iqOptionBotTrader/db.json', 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Erro ao ler o arquivo JSON' });
    }
    res.json(JSON.parse(data));
  });
});

app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, '../../views/index.html'));
})

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});