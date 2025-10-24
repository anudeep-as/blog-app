import os
import sys
from app import app
import init_db

if __name__ == '__main__':
    # Initialize the database
    print("Initializing database...")
    init_db.init_db()
    
    # Start the Flask application
    print("Starting Flask application...")
    print("Visit http://localhost:5000 to view the blog")
    print("Visit http://localhost:5000/admin to access the admin panel")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
