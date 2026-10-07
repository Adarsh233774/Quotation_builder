# Premium Quotation Management System

A production-ready Quotation Management Web Application built for architecture, interior design, and woodwork businesses. 

## Features
- **Dynamic Quotation Builder**: Create quotations with dynamic sections and items, calculated locally via HTMX without full page reloads.
- **Robust Calculation Engine**: Handles Fixed Amounts, Quantity \u00d7 Rate, and Length \u00d7 Width \u00d7 Rate using Python Decimals for absolute financial accuracy.
- **Excel Compatibility**: Fully reverse-engineers legacy Excel workbooks (e.g. `Common Temp.xlsx`), and supports exporting quotations back to an editable `.xlsx` format with native Excel formulas injected.
- **Document Generation**: One-click generation of professional `.docx` files ready to be sent to clients.
- **Premium UI**: Desktop-first layout customized with modern typography (Inter, Playfair Display) and responsive micro-animations.

## Technology Stack
- **Backend**: Python 3.9, Django 4.2
- **Frontend**: Django Templates, HTMX, Vanilla CSS
- **Database**: SQLite (Local) / PostgreSQL (Production)
- **Document Generation**: openpyxl, python-docx

## Installation & Setup

1. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Seed Database for Testing**
   (Creates a dummy Client and Project to test the UI)
   ```bash
   python seed.py
   ```

5. **Start Development Server**
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://127.0.0.1:8000/`

## Testing Excel Import & Export
To test the core Excel extraction engine without using the web UI:
1. Ensure `D:\MY\Dad Work\Common Temp.xlsx` exists.
2. Run `python import_test.py` to import the file into the database.
3. Run `python test_export.py` to test the `.xlsx` and `.docx` generation. Check the project root for the exported files.

## Production Deployment
- Ensure `DEBUG = False` in `config/settings.py`
- Configure `DATABASES` to point to a PostgreSQL instance via environment variables.
- Serve static files using Nginx or WhiteNoise.
- Bind the application with Gunicorn.
