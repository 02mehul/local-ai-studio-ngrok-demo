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

## 📁 Project Structure

```
local-ai-studio-ngrok-demo/
├── web/                          # Local vanilla JS frontend
│   ├── index.html                # Main HTML (with dynamic markers)
│   ├── app.js                    # App logic (with dynamic markers)
│   ├── styles.css                # Styling (CSS Grid layout)
│   ├── config.js                 # Supabase keys (git-ignored)
│   └── services/
│       └── todoService.js        # API service (with dynamic markers)
├── lovable/
│   └── todo-sanctuary/           # Cloned Lovable repo (see below)
│       └── db/migrations/        # Migration source folder (watched)
├── supabase/
│   └── migrations/               # Local Supabase migrations (target)
├── scripts/
│   ├── watch_migrations.ps1      # Migration watcher script
│   └── scaffold_ui.js            # Auto UI scaffolding script
├── start_safe.bat                # Main startup script
├── start_dev.ps1                 # Alternative PowerShell startup
└── prompts_used_in_migrations.txt # Prompts to generate migrations in Lovable
```

---

## 🔗 Lovable Repository (todo-sanctuary)

The `lovable/todo-sanctuary` folder contains a **clone** of the Lovable-generated frontend project.

### How to Clone

```bash
cd lovable
git clone https://github.com/02mehul/todo-sanctuary
```

This gives you the Lovable project locally, including any migration files that Lovable generates in `db/migrations/`.

### Why We Clone It

When you ask Lovable AI to create database migrations (e.g., adding a new column), it generates `.sql` files inside its own project at `db/migrations/`. By cloning this repo locally, our **Migration Watcher** script can detect these new files and automatically sync them to the local Supabase database.

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

### Phase 2: Clone the Lovable Repository

```bash
cd lovable
git clone https://github.com/02mehul/todo-sanctuary
```

### Phase 3: Start the Engine
We have a "Magic Script" that starts everything for you.

1.  Open **PowerShell** (or VS Code Terminal).
2.  Navigate to this project folder.
3.  Run this command:
    ```powershell
    .\start_safe.bat
    ```
4.  **Wait**. The first time you run this, it might take a few minutes to download the Database tools (Docker images).

**What the script does:**
*   ✅ Starts a Local Web Server (port 8000).
*   ✅ Opens the Ngrok Tunnel.
*   ✅ Starts the Supabase Database.
*   ✅ Starts the **Migration Watcher** (monitors `lovable/todo-sanctuary/db/migrations/`).
*   ✅ Prints your "Secret Keys" to the screen.

### Phase 4: Verify It Worked
Once the script stops scrolling, check these links:

*   **Web App**: [http://localhost:8000](http://localhost:8000) (You should see the app loading)
*   **Database Dashboard**: [http://127.0.0.1:54323](http://127.0.0.1:54323) (This is "Supabase Studio")
*   **Tunnel Status**: [http://localhost:4040](http://localhost:4040) (Shows your public URL)

---

## 🔄 Migration Automation System

This is the **core automation** of the project. When you create a new migration in Lovable, the entire pipeline runs automatically — no manual steps needed.

### How It Works (End-to-End Flow)

```
┌──────────────┐     git pull / paste      ┌──────────────────────────────────┐
│   Lovable    │  ──────────────────────►   │  lovable/todo-sanctuary/         │
│   (Cloud)    │   generates .sql file     │  db/migrations/                  │
└──────────────┘                           │  📄 new_migration.sql            │
                                           └──────────┬───────────────────────┘
                                                      │
                                          watch_migrations.ps1 detects it
                                                      │
                                           ┌──────────▼───────────────────────┐
                                           │  Step 1: COPY                    │
                                           │  Copy .sql → supabase/migrations │
                                           └──────────┬───────────────────────┘
                                                      │
                                           ┌──────────▼───────────────────────┐
                                           │  Step 2: SCAFFOLD UI             │
                                           │  scaffold_ui.js reads the SQL,   │
                                           │  detects ADD COLUMN, and auto-   │
                                           │  updates index.html, app.js,     │
                                           │  and todoService.js              │
                                           └──────────┬───────────────────────┘
                                                      │
                                           ┌──────────▼───────────────────────┐
                                           │  Step 3: APPLY TO DB             │
                                           │  Runs the SQL directly on the    │
                                           │  local Postgres via Docker exec  │
                                           └──────────────────────────────────┘
```

### Step-by-Step Breakdown

#### 1. Migration Watcher (`scripts/watch_migrations.ps1`)

This PowerShell script runs in the background and **polls** the `lovable/todo-sanctuary/db/migrations/` folder every 2 seconds for new `.sql` files.

When a new file is detected, it:
1.  **Copies** the file to `supabase/migrations/` (so Supabase knows about it).
2.  **Triggers** the UI scaffolding script (`scaffold_ui.js`).
3.  **Applies** the SQL directly to the running Postgres database via `docker exec`.

#### 2. UI Scaffolding (`scripts/scaffold_ui.js`)

This Node.js script **automatically updates the frontend** when a new column is added to the `todos` table. It works using a **marker-based injection** system.

**What it does:**
- Parses the migration SQL for `ALTER TABLE todos ADD COLUMN` statements.
- If it finds one, it injects the following into the frontend files:

| File | What Gets Added |
|---|---|
| `web/index.html` | A new `<input>` field for the column |
| `web/app.js` | A `getElementById` selector, data extraction, and clearing logic |
| `web/services/todoService.js` | A new parameter in `createTodo()` and the JSON payload |

**How the markers work:**

The frontend files contain special comment markers like:
```html
<!-- DYNAMIC_INPUT_FIELDS -->
```
```javascript
// DYNAMIC_ELEMENT_SELECTORS
// DYNAMIC_DATA_EXTRACTION
// DYNAMIC_DATA_CLEARING
/* DYNAMIC_PAYLOAD_FIELDS */
```

The scaffold script finds these markers and injects the new code **just before** them, then writes the marker back. This way, the next migration can inject code at the same spot.

> **Note:** The scaffolder only handles `ADD COLUMN` statements on the `todos` table. Other SQL operations (like `CREATE TABLE`) are applied to the DB but don't trigger UI changes.

#### 3. Database Application

The SQL is applied instantly via Docker:
```powershell
docker exec -i supabase_db_local-ai-studio-ngrok-demo psql -U postgres -c "<sql>"
```

No Supabase restart is needed — the column appears immediately in the database.

---

## 📝 Creating Migrations in Lovable

To create a new migration via **Lovable AI**, use the prompts below (also saved in `prompts_used_in_migrations.txt`).

> **Important:** Lovable creates files inside its own project. After Lovable generates the migration, either `git pull` in the `lovable/todo-sanctuary` folder, or manually paste the file into `lovable/todo-sanctuary/db/migrations/`. The watcher will pick it up automatically.

### Recommended Prompts - check file prompts_used_in_migrations.txt


```

### Migration File Naming Convention

Use this format: `YYYYMMDDHHMMSS_description.sql`

Example: `20260213105000_add_due_date_column.sql`

---

## 🔐 Configuration & Security

To keep your secrets safe, we do **not** upload your API keys to GitHub.

*   **`web/config.js`**: This file contains your actual keys. It is **ignored** by Git.
*   **`web/config.js.example`**: This is a template file.

**Tools**:
*   `.\start_dev.ps1`: Automatically generates `config.js` for you.
*   If you need to setup manually (without the script), copy `.example` to `.js` and fill in your keys.

---


---

## 🛑 Stopping Safely (Don't lose your data!)

When you are done for the day, **DO NOT** just close the terminal or delete Docker containers manually. This can cause data loss.

**Run this command:**
```powershell
.\stop_dev.ps1
```

This will:
*   ✅ Stop Supabase safely (saving your data).
*   ✅ Stop the Web Server and Ngrok.

**Next Morning:**
1.  Open Docker Desktop.
2.  Run `.\start_dev.ps1`.
3.  Your data will still be there!

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
