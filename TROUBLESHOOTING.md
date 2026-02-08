# Troubleshooting Guide

## Common Issues and Solutions

### 1. 404 Error on `/api/datasets/1/chart-data/`

**Problem:** Frontend calling `chart-data` but backend uses `chart_data`

**Solution:** ✅ FIXED - Updated frontend to use `chart_data` (underscore)

**Verify:** The URL should now be `/api/datasets/1/chart_data/`

---

### 2. 400 Error on Upload

**Possible Causes:**

1. **Backend not running**
   - Make sure Django server is running: `python manage.py runserver`
   - Check it's on port 8000

2. **CORS issues**
   - Check `CORS_ALLOWED_ORIGINS` in `backend/equipment_api/settings.py`
   - Should include `http://localhost:3000`

3. **File format issues**
   - CSV must have columns: `Equipment Name`, `Type`, `Flowrate`, `Pressure`, `Temperature`
   - File must end with `.csv`
   - Check browser console for specific error message

4. **File size too large**
   - Check if there's a file size limit

**Debug Steps:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try uploading a file
4. Click on the failed request
5. Check the Response tab for error details

---

### 3. Backend Not Responding

**Check:**
```cmd
cd backend
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**Test backend:**
- Open browser: `http://localhost:8000/api/datasets/`
- Should return JSON (empty array `[]` or list of datasets)

---

### 4. Frontend Not Connecting to Backend

**Check:**
1. Backend is running on port 8000
2. Frontend API URL in `frontend-web/src/services/api.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000/api';
   ```
3. CORS is enabled in Django settings

**Test:**
- Open browser console (F12)
- Check for CORS errors
- Check Network tab for failed requests

---

### 5. Charts Not Displaying

**Check:**
1. Dataset has equipment items
2. Chart data endpoint returns data:
   - `http://localhost:8000/api/datasets/1/chart_data/`
3. Browser console for JavaScript errors

---

## Quick Verification Checklist

- [ ] Backend server running on port 8000
- [ ] Can access `http://localhost:8000/api/datasets/` in browser
- [ ] Frontend running on port 3000
- [ ] Can access `http://localhost:3000` in browser
- [ ] No CORS errors in browser console
- [ ] Dataset exists (check `/api/datasets/`)
- [ ] Chart data endpoint works (`/api/datasets/1/chart_data/`)

---

## Testing Endpoints Manually

### Using Browser:
1. `http://localhost:8000/api/datasets/` - List datasets
2. `http://localhost:8000/api/datasets/1/` - Get dataset details
3. `http://localhost:8000/api/datasets/1/summary/` - Get summary
4. `http://localhost:8000/api/datasets/1/chart_data/` - Get chart data

### Using curl:
```cmd
curl http://localhost:8000/api/datasets/
curl http://localhost:8000/api/datasets/1/chart_data/
```

---

## Common Error Messages

**"Failed to load resource: 404"**
- URL doesn't exist
- Check URL spelling (underscore vs hyphen)
- Backend route not registered

**"Failed to load resource: 400"**
- Bad request
- Check request format
- Check file format for uploads
- Check required fields

**"CORS policy" errors**
- Backend CORS not configured
- Check `CORS_ALLOWED_ORIGINS` in settings

**"Network Error"**
- Backend not running
- Wrong port number
- Firewall blocking connection
