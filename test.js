const fs = require('fs');

const json = fs.readFileSync('./user_json.txt');

const data = JSON.parse(json);

console.log(data);