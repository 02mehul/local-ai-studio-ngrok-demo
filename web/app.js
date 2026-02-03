// Main App Logic
import { todoService } from './services/todoService.js';
import { CONFIG } from './config.js';

const statusEl = document.getElementById('status-bar');
const listEl = document.getElementById('todo-list');
const inputEl = document.getElementById('new-todo');
const priorityEl = document.getElementById('new-priority');
const addBtn = document.getElementById('add-btn');

// Status Check (Visual only)
function updateStatus() {
    if (CONFIG.SUPABASE_URL && CONFIG.SUPABASE_KEY) {
        statusEl.textContent = `Connected to: ${CONFIG.SUPABASE_URL} (${CONFIG.MODE})`;
        statusEl.style.color = 'green';
    } else {
        statusEl.textContent = 'Missing Configuration: Check .env or config.js';
        statusEl.style.color = 'red';
    }
}

// Render Todos
function renderTodos(todos) {
    listEl.innerHTML = '';

    if (!Array.isArray(todos)) {
        console.error("Expected array of todos, got:", todos);
        return;
    }

    todos.forEach(todo => {
        const li = document.createElement('li');
        li.className = todo.done ? 'done' : '';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = todo.done;
        // Optimization: don't await the toggle for UI responsiveness (optimistic could be better but keep simple)
        checkbox.onclick = () => toggleTodo(todo.id, !todo.done);

        const span = document.createElement('span');
        span.textContent = todo.title;

        if (todo.priority > 0) {
            const badge = document.createElement('span');
            badge.textContent = `P${todo.priority}`;
            badge.style.marginLeft = '8px';
            badge.style.fontSize = '0.8em';
            badge.style.padding = '2px 6px';
            badge.style.borderRadius = '4px';
            badge.style.backgroundColor = todo.priority === 3 ? '#ffe4e6' : (todo.priority === 2 ? '#ffedd5' : '#f1f5f9');
            badge.style.color = todo.priority === 3 ? '#e11d48' : (todo.priority === 2 ? '#c2410c' : '#475569');
            badge.style.fontWeight = 'bold';
            span.appendChild(badge);
        }

        const delBtn = document.createElement('button');
        delBtn.textContent = 'X';
        delBtn.style.marginLeft = '10px';
        delBtn.onclick = () => deleteTodo(todo.id);

        li.appendChild(checkbox);
        li.appendChild(span);
        li.appendChild(delBtn); // Added delete button
        listEl.appendChild(li);
    });
}

// Fetch Todos
async function fetchTodos() {
    try {
        const todos = await todoService.getTodos();
        renderTodos(todos);
    } catch (e) {
        console.error("Failed to fetch todos", e);
        statusEl.textContent = `Error: ${e.message}`;
        statusEl.style.color = 'red';
    }
}

// Add Todo
async function addTodo() {
    const title = inputEl.value.trim();
    if (!title) return;

    try {
        const priorityVal = priorityEl ? priorityEl.value : '0';
        console.log('Selected Priority Raw:', priorityVal);
        const priority = parseInt(priorityVal) || 0;
        console.log('Sending Priority:', priority);
        await todoService.createTodo(title, priority);
        inputEl.value = '';
        priorityEl.value = '0';
        fetchTodos();
    } catch (e) {
        console.error("Failed to add todo", e);
        alert(e.message);
    }
}

// Toggle Todo
async function toggleTodo(id, done) {
    try {
        await todoService.updateTodo(id, { done });
        fetchTodos();
    } catch (e) {
        console.error("Failed to toggle todo", e);
        alert(e.message);
    }
}

// Delete Todo
async function deleteTodo(id) {
    try {
        await todoService.deleteTodo(id);
        fetchTodos();
    } catch (e) {
        console.error("Failed to delete todo", e);
        alert(e.message);
    }
}

// Event Listeners
addBtn.onclick = addTodo;
inputEl.onkeypress = (e) => {
    if (e.key === 'Enter') addTodo();
};

// Init
updateStatus();
fetchTodos();
