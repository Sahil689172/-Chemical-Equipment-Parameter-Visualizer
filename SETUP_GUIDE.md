# Setup and Run Guide

## Quick Start Commands

### 1. Backend (Django) - Run in First Terminal

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py load_equipment
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**Backend will be running at:** `http://localhost:8000`

---

### 2. Frontend Web (React) - Run in Second Terminal

```cmd
cd frontend-web
npm install
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view chemical-equipment-visualizer-web in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Frontend will be running at:** `http://localhost:3000`

---

### 3. Frontend Desktop (PyQt5) - Optional - Run in Third Terminal

```cmd
cd frontend-desktop
pip install -r requirements.txt
python main.py
```

---

## Verification Steps

### Step 1: Check Backend is Running

1. Open browser and go to: `http://localhost:8000/api/datasets/`
2. **Expected:** You should see JSON data (either empty array `[]` or list of datasets)
3. If you see JSON, backend is working ✅

**Alternative check:**
```cmd
curl http://localhost:8000/api/datasets/
```

---

### Step 2: Check Frontend is Running

1. Open browser and go to: `http://localhost:3000`
2. **Expected:** You should see the Chemical Equipment Visualizer interface
3. If the page loads, frontend is working ✅

---

### Step 3: Test CSV Upload

1. In the web app, click "Upload Equipment Data"
2. Click "Browse" and select: `sample_data/sample_equipment_data.csv`
3. Click "Upload CSV"
4. **Expected:** 
   - Progress bar appears
   - Success message: "Successfully uploaded..."
   - Dataset appears in History tab
   - Data appears in Data Table tab
   - Charts appear in Charts tab

---

### Step 4: Verify API Endpoints

Test these URLs in your browser:

1. **List Datasets:**
   ```
   http://localhost:8000/api/datasets/
   ```
   Should return JSON with dataset list

2. **Get Dataset Details (replace 1 with your dataset ID):**
   ```
   http://localhost:8000/api/datasets/1/
   ```
   Should return dataset with equipment items

3. **Get Summary:**
   ```
   http://localhost:8000/api/datasets/1/summary/
   ```
   Should return summary statistics

4. **Get Chart Data:**
   ```
   http://localhost:8000/api/datasets/1/chart-data/
   ```
   Should return chart data in JSON format

---

### Step 5: Check Data Display

1. **Data Table Tab:**
   - Should show 20 equipment items
   - Columns: Equipment Name, Type, Flowrate, Pressure, Temperature
   - Table should be sortable

2. **Charts Tab:**
   - Bar chart showing flowrate by type
   - Scatter plot showing pressure vs temperature
   - Pie chart showing type distribution

3. **Summary Cards:**
   - Total Equipment Count: 20
   - Average Flowrate, Pressure, Temperature displayed

---

## Troubleshooting

### Backend Issues

**Problem: ModuleNotFoundError: No module named 'django'**
```cmd
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Problem: Port 8000 already in use**
```cmd
python manage.py runserver 8001
```
Then update frontend API URL in `frontend-web/src/services/api.js`

**Problem: Database errors**
```cmd
cd backend
python manage.py migrate
python manage.py load_equipment
```

---

### Frontend Issues

**Problem: npm install fails**
```cmd
cd frontend-web
npm cache clean --force
npm install
```

**Problem: Port 3000 already in use**
- React will automatically ask to use port 3001
- Or set port manually:
```cmd
set PORT=3001
npm start
```

**Problem: Cannot connect to API**
- Check backend is running on port 8000
- Check CORS settings in `backend/equipment_api/settings.py`
- Verify API URL in `frontend-web/src/services/api.js`

---

### Common Issues

**CORS Error:**
- Make sure `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` includes `http://localhost:3000`

**Empty Data:**
- Run: `python manage.py load_equipment` to load sample data
- Or upload CSV file through the web interface

**Charts Not Displaying:**
- Check browser console for errors
- Verify chart data endpoint returns valid JSON
- Make sure dataset has equipment items

---

## Complete Test Checklist

- [ ] Backend server starts without errors
- [ ] Can access `http://localhost:8000/api/datasets/` in browser
- [ ] Frontend web app loads at `http://localhost:3000`
- [ ] Can upload CSV file successfully
- [ ] Data appears in Data Table tab
- [ ] Charts display correctly (3 charts visible)
- [ ] Summary cards show correct statistics
- [ ] History tab shows uploaded datasets
- [ ] Can switch between datasets in History
- [ ] Table is sortable by clicking column headers
- [ ] All API endpoints return valid JSON

---

## Quick Test Script

Save this as `test_api.bat` and run it:

```batch
@echo off
echo Testing Backend API...
curl http://localhost:8000/api/datasets/
echo.
echo.
echo If you see JSON data above, backend is working!
echo Open http://localhost:3000 in your browser to test frontend.
pause
```

---

## Production Notes

For production deployment:
- Change `DEBUG = False` in Django settings
- Update `ALLOWED_HOSTS` in Django settings
- Build React app: `npm run build`
- Use production web server (nginx, Apache)
- Use production WSGI server (gunicorn, uWSGI)
