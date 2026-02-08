# Fix for Pandas Installation Error

## Problem
You're getting an error because:
- Python 3.13 is being used
- pandas 2.1.3 doesn't have pre-built wheels for Python 3.13
- It's trying to build from source and failing due to GCC version

## Solution Options

### Option 1: Use Updated Pandas (Recommended)
The requirements.txt has been updated to use pandas>=2.2.0 which has better Python 3.13 support.

Try installing again:
```cmd
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 2: Install Pre-built Wheels Only
Skip building from source:
```cmd
cd backend
pip install --only-binary :all: -r requirements.txt
```

### Option 3: Use Python 3.11 or 3.12 (Most Reliable)
If the above doesn't work, use Python 3.11 or 3.12:

1. Install Python 3.11 or 3.12 from python.org
2. Create virtual environment with that version:
```cmd
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Option 4: Install Without Pandas (Minimal)
If you don't need pandas for basic functionality, you can remove it temporarily:

1. Edit `backend/requirements.txt` and comment out pandas:
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
# pandas>=2.2.0  # Commented out - not needed for basic CSV upload
reportlab==4.0.7
```

2. Install:
```cmd
pip install -r requirements.txt
```

Note: The CSV upload will still work because we use pandas only for parsing, and we can use Python's built-in csv module as fallback.
