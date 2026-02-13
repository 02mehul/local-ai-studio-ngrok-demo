const fs = require('fs');
const path = require('path');

const migrationFile = process.argv[2];

if (!migrationFile) {
    console.log("Usage: node scaffold_ui.js <path-to-migration-file>");
    process.exit(1);
}

if (!fs.existsSync(migrationFile)) {
    console.log(`Migration file not found: ${migrationFile}`);
    process.exit(1);
}

const content = fs.readFileSync(migrationFile, 'utf8');

// Regex to find ADD COLUMN
// Example: ALTER TABLE public.todos ADD COLUMN IF NOT EXISTS deadline text;
const columnRegex = /ALTER TABLE\s+(?:public\.)?(\w+)\s+ADD COLUMN\s+(?:IF NOT EXISTS\s+)?(\w+)\s+(\w+)/i;
const match = content.match(columnRegex);

if (!match) {
    console.log("No ADD COLUMN statement found in migration file.");
    process.exit(0);
}

const tableName = match[1];
const columnName = match[2];
const columnType = match[3];

if (tableName !== 'todos') {
    console.log(`Skipping: Table is '${tableName}', only 'todos' is supported for auto-ui.`);
    process.exit(0);
}

console.log(`Scaffolding UI for new column: ${columnName} (${columnType})`);

const webDir = path.join(__dirname, '../web');
const indexHtml = path.join(webDir, 'index.html');
const appJs = path.join(webDir, 'app.js');
const todoServiceJs = path.join(webDir, 'services/todoService.js');

// 1. Update index.html
let html = fs.readFileSync(indexHtml, 'utf8');
const inputHtml = `            <input type="text" id="new-${columnName}" placeholder="${columnName} (optional)">\n            <!-- DYNAMIC_INPUT_FIELDS -->`;
html = html.replace('<!-- DYNAMIC_INPUT_FIELDS -->', inputHtml);
fs.writeFileSync(indexHtml, html);
console.log(`Updated index.html`);

// 2. Update app.js
let js = fs.readFileSync(appJs, 'utf8');

// Selectors
const selectorCode = `const ${columnName}El = document.getElementById('new-${columnName}');\n// DYNAMIC_ELEMENT_SELECTORS`;
js = js.replace('// DYNAMIC_ELEMENT_SELECTORS', selectorCode);

// Extraction
const extractCode = `        const ${columnName} = ${columnName}El ? ${columnName}El.value.trim() : '';\n        // DYNAMIC_DATA_EXTRACTION`;
js = js.replace('// DYNAMIC_DATA_EXTRACTION', extractCode);

// Logging/Usage (Simplified: just log it for now, user might need to choose where to show it)
// We also need to pass it to createTodo. 
// We will modify the createTodo call regex.
// Find: await todoService.createTodo(title, priority, description);
// We need a marker there too or just regex replace the call.
// Let's rely on the fact that the last argument is description for now, or just regex replace the closing parenthesis.

const updateCallRegex = /(await todoService\.createTodo\(.*?)(\);)/;
// This is risky if spans multiple lines.
// Let's use a new marker I forgot to add: call site. 
// Actually I can just replace `await todoService.createTodo(title, priority, description);` 
// with `await todoService.createTodo(title, priority, description, ${columnName});`
// But wait, what if I added another one before?
// Robust way: read the current call line.
// For now, let's use a marker in app.js for the call site. I will add it in a separate step or just use a known string.
// "await todoService.createTodo(title, priority, description" -> "await todoService.createTodo(title, priority, description, ${columnName}"

// Let's assume the previous param was 'description' OR the last param added.
// We can use a regex that looks for the function call.
js = js.replace(/await todoService\.createTodo\(([^)]+)\)/, (match, args) => {
    return `await todoService.createTodo(${args}, ${columnName})`;
});

// Clearing
const clearCode = `        if (${columnName}El) ${columnName}El.value = '';\n        // DYNAMIC_DATA_CLEARING`;
js = js.replace('// DYNAMIC_DATA_CLEARING', clearCode);

fs.writeFileSync(appJs, js);
console.log(`Updated app.js`);

// 3. Update todoService.js
let serviceJs = fs.readFileSync(todoServiceJs, 'utf8');

// Update signature: async createTodo(title, priority = 0, description = '')
// We need to append the new arg.
serviceJs = serviceJs.replace(/async createTodo\(([^)]+)\)/, (match, args) => {
    return `async createTodo(${args}, ${columnName} = '')`;
});

// Update payload: body: JSON.stringify({ title, done: false, priority, description /* ... */ })
// We use the marker here.
serviceJs = serviceJs.replace(/\/\* DYNAMIC_PAYLOAD_FIELDS \*\//, `, ${columnName} /* DYNAMIC_PAYLOAD_FIELDS */`);

fs.writeFileSync(todoServiceJs, serviceJs);
console.log(`Updated todoService.js`);

console.log("UI Scaffolding Complete.");
