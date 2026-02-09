# Commands to Run Backend and Frontend

## Backend (Django)

### First Time Setup:
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if using one)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run migrations (if not already done)
python manage.py migrate
```

### Run Backend Server:
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if using one)
venv\Scripts\activate

# Run Django development server
python manage.py runserver
```

**Backend will run on:** `http://localhost:8000`

---

## Frontend Web (React)

### First Time Setup:
```bash
# Navigate to frontend-web directory
cd frontend-web

# Install dependencies (if not already installed)
npm install
```

### Run Frontend Web:
```bash
# Navigate to frontend-web directory
cd frontend-web

# Start React development server
npm start
```

**Frontend Web will run on:** `http://localhost:3000`

---

## Frontend Desktop (PyQt5)

### First Time Setup:
```bash
# Navigate to frontend-desktop directory
cd frontend-desktop

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

### Run Frontend Desktop:
```bash
# Navigate to frontend-desktop directory
cd frontend-desktop

# Run the desktop application
python main.py
```

---

## Quick Start (All Services)

### Terminal 1 - Backend:
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

### Terminal 2 - Frontend Web:
```bash
cd frontend-web
npm start
```

### Terminal 3 - Frontend Desktop (Optional):
```bash
cd frontend-desktop
python main.py
```

---

## Important Notes:

1. **Backend must be running first** before starting frontend applications
2. **Backend runs on:** `http://localhost:8000`
3. **Frontend Web runs on:** `http://localhost:3000`
4. Make sure Django backend is accessible before using the desktop app
5. For Windows, use `venv\Scripts\activate` to activate virtual environment
6. For Linux/Mac, use `source venv/bin/activate` to activate virtual environment

---

## Troubleshooting:

### Backend Issues:
- If port 8000 is busy: `python manage.py runserver 8001`
- If migrations needed: `python manage.py migrate`
- Check Django is installed: `pip list | findstr Django`

### Frontend Web Issues:
- If port 3000 is busy, React will ask to use another port
- Clear cache: `npm cache clean --force`
- Reinstall: `rm -rf node_modules && npm install`

### Frontend Desktop Issues:
- Make sure PyQt5 is installed: `pip install PyQt5`
- Check backend is running before using desktop app
- Verify API connection in desktop app
