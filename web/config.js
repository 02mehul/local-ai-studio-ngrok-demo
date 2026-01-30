const ENV = window.env || {};

export const CONFIG = {
    // Default to Local Supabase (Docker)
    SUPABASE_URL: 'http://127.0.0.1:54321',
    SUPABASE_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0',
    USE_NGROK: ENV.VITE_USE_NGROK === 'true',
    MODE: ENV.VITE_SUPABASE_MODE || 'rest', // 'rest' | 'client'
};

export const API_ENDPOINTS = {
    TODOS: '/rest/v1/todos',
};
