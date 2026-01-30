// import { API_BASE_URL, API_ENDPOINTS } from '../constants';
// import { TodoItem, TodoCreate, TodoUpdate } from '../types';

// class TodoService {
//   private async request<T>(
//     endpoint: string,
//     options: RequestInit = {}
//   ): Promise<T> {
//     const url = `${API_BASE_URL}${endpoint}`;

//     // Add ngrok bypass header so fetch() does NOT receive the ngrok HTML interstitial page.
//     // Also set Accept header to ensure we get JSON.
//     const headers: Record<string, string> = {
//       'Accept': 'application/json',
//       'ngrok-skip-browser-warning': 'true',
//       ...(options.headers as Record<string, string>),
//     };

//     // Only set Content-Type automatically when sending a body.
//     // (GET/DELETE don't need it, but it also usually doesn't hurt.)
//     const hasBody = options.body !== undefined && options.body !== null;
//     if (hasBody && !headers['Content-Type']) {
//       headers['Content-Type'] = 'application/json';
//     }

//     const response = await fetch(url, { ...options, headers });

//     if (!response.ok) {
//       // Response might be JSON or HTML; try to read text safely.
//       const raw = await response.text().catch(() => '');
//       try {
//         const errorJson = raw ? JSON.parse(raw) : {};
//         throw new Error(
//           errorJson?.detail?.[0]?.msg ||
//             errorJson?.message ||
//             response.statusText ||
//             'API Request failed'
//         );
//       } catch {
//         // If it's HTML (ngrok interstitial), this gives a helpful error message.
//         throw new Error(
//           raw?.includes('<!DOCTYPE')
//             ? 'API returned HTML instead of JSON (ngrok warning page). Ensure ngrok-skip-browser-warning header is sent and ngrok URL is correct.'
//             : response.statusText || 'API Request failed'
//         );
//       }
//     }

//     // Successful response should be JSON array per spec
//     const text = await response.text();
//     try {
//       return JSON.parse(text) as T;
//     } catch {
//       // If we got HTML again, make it obvious.
//       if (text.includes('<!DOCTYPE')) {
//         throw new Error(
//           'API returned HTML instead of JSON (ngrok warning page). Ensure ngrok-skip-browser-warning header is sent and ngrok URL is correct.'
//         );
//       }
//       throw new Error('Failed to parse JSON response from API.');
//     }
//   }

//   async getTodos(): Promise<TodoItem[]> {
//     return this.request<TodoItem[]>(API_ENDPOINTS.TODOS);
//   }

//   async createTodo(todo: TodoCreate): Promise<TodoItem[]> {
//     return this.request<TodoItem[]>(API_ENDPOINTS.TODOS, {
//       method: 'POST',
//       body: JSON.stringify(todo),
//     });
//   }

//   async updateTodo(id: number, updates: TodoUpdate): Promise<TodoItem[]> {
//     const endpoint = `${API_ENDPOINTS.TODOS}?id=eq.${id}`;
//     return this.request<TodoItem[]>(endpoint, {
//       method: 'PATCH',
//       body: JSON.stringify(updates),
//     });
//   }

//   async deleteTodo(id: number): Promise<TodoItem[]> {
//     const endpoint = `${API_ENDPOINTS.TODOS}?id=eq.${id}`;
//     return this.request<TodoItem[]>(endpoint, {
//       method: 'DELETE',
//     });
//   }
// }

// export const todoService = new TodoService();
