# Chemical Equipment Parameter Visualizer

A hybrid application for visualizing chemical equipment parameters with three interfaces:
- **Django REST API Backend** - Provides data management and API endpoints
- **React Web Application** - Modern web interface with interactive charts
- **PyQt5 Desktop Application** - Native desktop client for data visualization

## Project Structure

```
project/
├── backend/                 # Django backend
│   ├── equipment_api/      # Main Django app
│   ├── requirements.txt
│   └── manage.py
├── frontend-web/           # React web app
│   ├── src/
│   ├── package.json
│   └── public/
├── frontend-desktop/       # PyQt5 desktop app
│   ├── main.py
│   ├── requirements.txt
│   └── ui/
├── sample_data/
│   └── sample_equipment_data.csv
└── README.md
```

## Features

- **Equipment Data Management**: Store and manage chemical equipment parameters
- **RESTful API**: Django REST Framework API for data access
- **Web Visualization**: Interactive charts and tables using React and Recharts
- **Desktop Client**: Native PyQt5 application for offline data viewing
- **CSV Import/Export**: Support for CSV data import and export

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- pip (Python package manager)

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. (Optional) Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

6. Load sample data:
```bash
python manage.py load_equipment
```
Or specify a custom CSV file:
```bash
python manage.py load_equipment ../sample_data/sample_equipment_data.csv
```

7. Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/equipment/`

### Web Frontend Setup

1. Navigate to the frontend-web directory:
```bash
cd frontend-web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The web app will be available at `http://localhost:3000`

### Desktop Application Setup

1. Navigate to the frontend-desktop directory:
```bash
cd frontend-desktop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Web Application

- Open `http://localhost:3000` in your browser
- The application will automatically fetch data from the Django API
- View interactive charts and equipment tables
- Ensure the Django backend is running on port 8000

### Desktop Application

- Launch the application using `python main.py`
- Click "Load from CSV" to import data from a CSV file
- Click "Load from API" to fetch data from the Django backend
- View equipment data in a table format with statistics

### API Endpoints

- `GET /api/equipment/` - List all equipment
- `GET /api/equipment/{id}/` - Get specific equipment details
- `POST /api/equipment/` - Create new equipment
- `PUT /api/equipment/{id}/` - Update equipment
- `DELETE /api/equipment/{id}/` - Delete equipment
- `GET /api/equipment/stats/` - Get equipment statistics

### Sample Data

The project includes a sample CSV file with 20 rows of realistic chemical equipment data:
- Equipment Name
- Type
- Flowrate (L/min)
- Pressure (bar)
- Temperature (°C)

## Development

### Backend Development

The Django backend uses:
- Django 4.2.7
- Django REST Framework 3.14.0
- django-cors-headers for CORS support

### Frontend Web Development

The React app uses:
- React 18.2.0
- Recharts for data visualization
- Axios for API calls

### Desktop Application Development

The PyQt5 app uses:
- PyQt5 5.15.10
- Requests for API communication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.
