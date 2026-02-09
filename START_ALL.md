# Quick Start Commands

## Prerequisites
- Python 3.8+ installed
- Node.js 14+ installed
- Virtual environment activated (for backend)

---

## 1. Backend (Django)

### First Time Setup:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
```

### Run Backend:
```bash
cd backend
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac
python manage.py runserver
```

**Backend will run on:** http://localhost:8000

---

## 2. Frontend Web (React)

### First Time Setup:
```bash
cd frontend-web
npm install
```

### Run Frontend Web:
```bash
cd frontend-web
npm start
```

**Frontend Web will run on:** http://localhost:3000

---

## 3. Frontend Desktop (PyQt5)

### First Time Setup:
```bash
cd frontend-desktop
pip install -r requirements.txt
```

### Run Frontend Desktop:
```bash
cd frontend-desktop
python main.py
```

---

## Running All Three Together

### Option 1: Three Separate Terminal Windows

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Frontend Web:**
```bash
cd frontend-web
npm start
```

**Terminal 3 - Frontend Desktop:**
```bash
cd frontend-desktop
python main.py
```

### Option 2: Using Batch File (Windows)

Create a `start_all.bat` file:
```batch
@echo off
start "Backend" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"
timeout /t 3
start "Frontend Web" cmd /k "cd frontend-web && npm start"
timeout /t 3
start "Frontend Desktop" cmd /k "cd frontend-desktop && python main.py"
```

Then run:
```bash
start_all.bat
```

---

## Important Notes

1. **Backend must be running first** before starting frontends
2. **Authentication required**: You'll need to register/login before using the app
3. **Database**: Make sure to run migrations: `python manage.py migrate`
4. **Ports**:
   - Backend: 8000
   - Frontend Web: 3000
   - Frontend Desktop: No port (desktop app)

---

## Troubleshooting

### Backend Issues:
- Make sure virtual environment is activated
- Run `python manage.py migrate` if you see database errors
- Check if port 8000 is already in use

### Frontend Web Issues:
- Make sure Node.js is installed: `node --version`
- Delete `node_modules` and run `npm install` again if needed
- Check if port 3000 is already in use

### Frontend Desktop Issues:
- Make sure PyQt5 is installed: `pip install PyQt5`
- Make sure backend is running before starting desktop app
- Check Python version: `python --version` (should be 3.8+)

---

## Quick Test

1. Start backend: `cd backend && venv\Scripts\activate && python manage.py runserver`
2. Open browser: http://localhost:8000/api/auth/register/
3. Register a new user
4. Start frontend web: `cd frontend-web && npm start`
5. Login with your credentials
6. Start desktop app: `cd frontend-desktop && python main.py`
7. Login with same credentials
