# 🧠 Cloud Brain + Local Body (Lovable + Supabase Demo)

Welcome! This project is a demonstration of a powerful, modern development workflow.

We use **Lovable AI** (running in the cloud) to build our frontend code, but we keep our data secure on our own **Local Supabase** database (running on this computer).

---

## 🏗️ Architecture Explained (Simply)

Imagine your project is a **Remote Control Car**:

1.  **The Car (Your Database)**: This is **Supabase**. It lives *inside* your computer ("Localhost") and holds all your data.
2.  **The Remote (The AI)**: This is **Lovable**. It lives *outside* in the cloud. It wants to "drive" your car (read/write data).
3.  **The Tunnel (Ngrok)**: Because your computer is private, Lovable can't see it. **Ngrok** opens a secure "Tunnel" so Lovable can send signals to your car.

---

## 🚀 Step-by-Step Setup Guide

Follow these instructions to start the project.

### Phase 1: Install Prerequisites
Before you begin, ensure you have these 4 tools installed:

1.  **Docker Desktop**: [Download Here](https://www.docker.com/products/docker-desktop/). (Must be open and running)
2.  **Node.js**: [Download Here](https://nodejs.org/). (Version 18+ recommended)
3.  **Python**: [Download Here](https://www.python.org/). (Version 3.x)
4.  **Ngrok**: [Download Here](https://ngrok.com/).
    *   *Important*: After installing, run `ngrok config add-authtoken <your-token>` in your terminal.

### Phase 2: Start the Engine
We have a "Magic Script" that starts everything for you.

1.  Open **PowerShell** (or VS Code Terminal).
2.  Navigate to this project folder.
3.  Run this command:
    ```powershell
    .\start_dev.ps1
    ```
4.  **Wait**. The first time you run this, it might take a few minutes to download the Database tools (Docker images).

**What the script does:**
*   ✅ Starts a Local Web Server.
*   ✅ Opens the Ngrok Tunnel.
*   ✅ Starts the Supabase Database.
*   ✅ Prints your "Secret Keys" to the screen.

### Phase 3: Verify It Worked
Once the script stops scrolling, check these links:

*   **Web App**: [http://localhost:8000](http://localhost:8000) (You should see the app loading)
*   **Database Dashboard**: [http://127.0.0.1:54323](http://127.0.0.1:54323) (This is "Supabase Studio")
*   **Tunnel Status**: [http://localhost:4040](http://localhost:4040) (Shows your public URL)

---


---

## 🔐 Configuration & Security

To keep your secrets safe, we do **not** upload your API keys to GitHub.

*   **`web/config.js`**: This file contains your actual keys. It is **ignored** by Git.
*   **`web/config.js.example`**: This is a template file.

**Tools**:
*   `.\start_dev.ps1`: Automatically generates `config.js` for you.
*   If you need to setup manually (without the script), copy `.example` to `.js` and fill in your keys.

---

## 🤖 How to Build with Lovable

Now that your "Local Body" (Database) is running, let's connect the "Cloud Brain" (Lovable).

### 1. Open Lovable
Go to [Lovable.dev](https://lovable.dev) and start a new project.

### 2. Copy the Master Prompt
Copy the **entire block of text below**. It contains everything Lovable needs: your database structure, your specific keys, and security fixes.

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
const supabaseUrl = 'YOUR_NGROK_URL';
const supabaseKey = 'YOUR_SUPABASE_KEY';

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

### 3. Paste and Go!
Paste that into Lovable's chat. It should build your full app in one shot.

---

## ❓ Troubleshooting

### "SyntaxError: Unexpected token '<'"
**Problem**: The app is trying to talk to the database but getting an HTML "Security Check" page from Ngrok instead.
**Solution**: This means the `ngrok-skip-browser-warning` header is missing. Make sure your code looks exactly like the "Connection Details" section in the Master Prompt above.

### "Connection Refused" / "Fetch Error"
**Problem**: The app can't reach the database at all.
**Solution**:
1. Is **Docker** running? (Look for the whale icon).
2. Did you run `.\start_dev.ps1`?
3. Did the Ngrok URL change? (Free Ngrok URLs change every time you restart. Check the terminal output and update your code).

### "Supabase is not starting"
**Solution**:
1. Stop everything: `npx supabase stop --no-backup`
2. Run the start script again: `.\start_dev.ps1`

### "Missing Config"
**Problem**: web/config.js is missing (it's ignored by Git).
**Solution**:
1. Run .\start_dev.ps1 (it auto-generates the file).
2. Or copy web/config.js.example to web/config.js and fill in your keys manually.
