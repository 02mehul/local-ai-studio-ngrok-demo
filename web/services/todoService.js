import { CONFIG, API_ENDPOINTS } from '../config.js';

export class TodoService {
    constructor() {
        this.baseUrl = CONFIG.SUPABASE_URL;
        this.key = CONFIG.SUPABASE_KEY;
        this.useNgrok = CONFIG.USE_NGROK;

        // Headers for Supabase PostgREST
        this.headers = {
            'apikey': this.key,
            'Authorization': `Bearer ${this.key}`,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation' // Important for getting back the object after insert/update
        };

        if (this.useNgrok) {
            this.headers['ngrok-skip-browser-warning'] = 'true';
        }
    }

    async _fetch(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.headers,
                ...options.headers
            }
        };

        const res = await fetch(url, config);

        if (!res.ok) {
            const text = await res.text();
            let errorMsg = res.statusText;
            try {
                const json = JSON.parse(text);
                errorMsg = json.message || json.error || json.hint || text;
            } catch (e) {
                errorMsg = text || res.statusText;
            }
            throw new Error(`API Error: ${errorMsg}`);
        }

        // Handle empty responses (like 204 No Content for delete if preference isn't set)
        if (res.status === 204) return null;

        return res.json();
    }

    async getTodos() {
        // GET /rest/v1/todos?select=*&order=priority.desc,id.desc
        return this._fetch(`${API_ENDPOINTS.TODOS}?select=*&order=priority.desc,id.desc`);
    }

    async createTodo(title, priority = 0, description = '', created_at = '') {
        console.log('SERVICE RECEIVED DESCRIPTION:', description); // DEBUG LOG
        // POST /rest/v1/todos
        return this._fetch(API_ENDPOINTS.TODOS, {
            method: 'POST',
            body: JSON.stringify({ title, done: false, priority, description, created_at /* DYNAMIC_PAYLOAD_FIELDS */ })
        });
    }

    async updateTodo(id, updates) {
        // PATCH /rest/v1/todos?id=eq.{id}
        // Body: { done: true/false }
        return this._fetch(`${API_ENDPOINTS.TODOS}?id=eq.${id}`, {
            method: 'PATCH',
            body: JSON.stringify(updates)
        });
    }

    async deleteTodo(id) {
        // DELETE /rest/v1/todos?id=eq.{id}
        return this._fetch(`${API_ENDPOINTS.TODOS}?id=eq.${id}`, {
            method: 'DELETE'
        });
    }
}

export const todoService = new TodoService();
