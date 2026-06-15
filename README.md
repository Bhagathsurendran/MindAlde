# 🧠 MindAIde — AI Mental Health Support System

> A Flask-based Mental Health Support System with AI Chatbot, Quiz Assessment, Self-Care Recommendations, and Therapist Management.

> [!WARNING]
> **If the ZIP includes a `venv` folder — delete it before setup.** Virtual environments contain hardcoded paths from the original machine and will not work on a different computer. You must create a fresh one (Step 2 below).
>
> **Never share the `.env` file.** It contains private API keys. Each person must create their own.

---

## ⚙️ Prerequisites (install these first)

| Requirement | Download Link |
|---|---|
| Python 3.10+ | https://www.python.org/downloads/ |
| MongoDB Community | https://www.mongodb.com/try/download/community |
| Google Gemini API Key | https://aistudio.google.com/app/apikey |

> **Python install tip:** Check ✅ "Add Python to PATH" during setup.

---

## 🚀 Setup Steps

### 1. Open a terminal in this folder
Right-click the folder → **Open in Terminal** (or use `cd` to navigate here).

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
```bash
# Windows Command Prompt:
venv\Scripts\activate

# Windows PowerShell:
venv\Scripts\Activate.ps1

# Mac / Linux:
source venv/bin/activate
```
You'll see `(venv)` at the start of your terminal line.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure your `.env` file
Open the `.env` file in any text editor and fill in:
```
GEMINI_API_KEY=paste_your_gemini_api_key_here
SECRET_KEY=any_long_random_string_here
```
> Get a free Gemini API key at https://aistudio.google.com/app/apikey

### 6. Make sure MongoDB is running
- Open Windows Services (`Win + R` → `services.msc`) → find **MongoDB** → click **Start**

### 7. (First time only) Seed self-care data
```bash
python seed_selfcare.py
```

### 8. Run the app
```bash
python app.py
```

### 9. Open in browser
```
http://127.0.0.1:5000
```

---

## 👤 User Roles

| Role | Access |
|---|---|
| **Admin** | Full control: users, quiz, therapists, resources |
| **Patient** | Quiz, chatbot, self-care, therapist finder |
| **Therapist** | Patient recommendations dashboard |
| **Caretaker** | Monitor a linked patient |

Register with role **Admin** first to access the admin panel.

---

## ✅ Quick Checklist

- [ ] Python 3.10+ installed (added to PATH)
- [ ] MongoDB installed and running
- [ ] `(venv)` is active in terminal
- [ ] `pip install -r requirements.txt` completed
- [ ] `.env` file has `GEMINI_API_KEY` and `SECRET_KEY` filled in
- [ ] `python app.py` is running
- [ ] Browser opened at `http://127.0.0.1:5000`
- [ ] Admin account created on first login
- [ ] `python seed_selfcare.py` run (if self-care page is empty)

---

## 🛠️ Common Issues

| Problem | Fix |
|---|---|
| `python` not recognized | Reinstall Python with "Add to PATH" checked |
| `ModuleNotFoundError` | Make sure `(venv)` is active, then re-run pip install |
| MongoDB not connecting | Start MongoDB from Windows Services |
| Chatbot not replying | Check Gemini API key is valid and has quota |
| `.env` not found | Enable "Show hidden files" in Windows Explorer |
| Port 5000 in use | Close the other app using port 5000 |
