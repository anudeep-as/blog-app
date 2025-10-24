@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Initializing database...
python init_db.py

echo.
echo Starting Flask application...
echo Visit http://localhost:5000 to view the blog
echo Visit http://localhost:5000/admin to access the admin panel
echo Press Ctrl+C to stop the server
echo.

python run.py
