# Local Supabase + Lovable AI Demo

This project demonstrates a **"Cloud Brain, Local Body"** architecture. It allows you to build a stunning React application using **Lovable AI** (the Brain) that connects securely to your **Local Supabase** database (the Body) running on your machine.

---

## 🚀 Junior Developer Setup Guide

Follow these steps exactly to get the project running on your local machine.

### 1. Prerequisites
Ensure you have these installed:
*   **Docker Desktop** (Must be running)
*   **Node.js** (LTS version)
*   **Python** (3.x)
*   **Ngrok** (Installed and authenticated)

### 2. Start the Stack
We have a master script that starts everything in the correct order:
1.  Starts the file server for the local web app.
2.  Opens the Ngrok tunnel.
3.  Starts the Supabase Docker containers.
4.  Auto-configures the app with your keys.

**Run this command in PowerShell:**
```powershell
.\start_dev.ps1
```

### 3. Verify It's Working
Once the script finishes:
*   **Web UI**: [http://localhost:8000](http://localhost:8000) (Should show the app)
*   **Supabase Studio**: [http://127.0.0.1:54323](http://127.0.0.1:54323) (Database Dashboard)
*   **Ngrok Dashboard**: [http://localhost:4040](http://localhost:4040) (To see your public URL)

---

## 🤖 How to Build with Lovable AI

To let Lovable build your frontend, you need to give it access to your local database via the tunnel. We have prepared a **Master Prompt** that sets up everything correctly, including the necessary security fixes.

### The Master Prompt
**Copy and paste everything below into Lovable:**

```markdown
I need you to build a modern, beautiful React application that connects to my **Local Supabase** instance via a secure Ngrok tunnel.

### 1. Technical Stack
- **Framework**: React + Vite
- **Styling**: Tailwind CSS + Shadcn/UI
- **Backend**: Supabase JS Client
- **Icons**: Lucide React

### 2. Connection Details (CRITICAL)
You must initialize the Supabase client exactly like this to bypass Ngrok security warnings:

'''typescript
import { createClient } from '@supabase/supabase-js';

// REPLACE these with your actual values from the terminal output if they change
const supabaseUrl = 'https://unharping-paulene-overslowly.ngrok-free.dev';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0';

export const supabase = createClient(supabaseUrl, supabaseKey, {
  global: {
    headers: { 'ngrok-skip-browser-warning': 'true' },
  },
});
'''

### 3. Data Model
Table: `todos`
- `id` (int8, primary key)
- `title` (text)
- `done` (boolean)
- `priority` (int4, default: 0)
- `created_at` (timestamptz)

### 4. Priority System (IMPORTANT)
Please implement the following **4-Level Priority System** to match my database:
- **0 = Normal** (Default, Gray badge)
- **1 = Low** (Blue badge)
- **2 = Medium** (Orange badge)
- **3 = High** (Red badge)
Ensure sorting puts High priority items at the top.

### 5. Requirements
1.  **Read**: Fetch todos sorted by priority (DESC) then created_at (DESC).
2.  **Create**: Form with Title and Priority dropdown.
3.  **Update**: Toggle 'done' status and change priority.
4.  **Delete**: Button to remove items.
5.  **Design**: Clean, dark mode aesthetic.
```

---

## 📂 Architecture

```mermaid
graph TD
    subgraph "The Cloud (Lovable)"
        AI[Lovable Generated App]
    end

    subgraph "Your Machine (Localhost)"
        Ngrok[Ngrok Tunnel]
        
        subgraph "Docker Containers"
            API[Supabase API :54321]
            DB[(Postgres DB)]
        end
    end

    AI -- "HTTPS + Auth Headers" --> Ngrok
    Ngrok -- "Secure Tunnel" --> API
    API -- "Query" --> DB
```

### Why use Ngrok?
Your local database (`localhost`) is invisible to the internet. Ngrok creates a secure "Door" that allows Lovable to talk to your database during development.

---

## 🛠️ Troubleshooting

**"SyntaxError: Unexpected token '<'"**
*   **Cause**: The app is hitting the Ngrok "Browser Warning" page instead of the API.
*   **Fix**: Ensure your `createClient` config includes the `ngrok-skip-browser-warning` header (included in the Master Prompt above).

**"Connection Refused"**
*   **Cause**: Docker is not running.
*   **Fix**: Restart Docker Desktop and run `.\start_dev.ps1` again.
