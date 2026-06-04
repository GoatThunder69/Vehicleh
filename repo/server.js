
const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname)));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'api-manager.html'));
});

app.listen(PORT, () => {
  console.log(`Gateway Manager running on port ${PORT}`);
});
