# BRAIN INSIGHT BLOG App

A responsive blog application with admin features built with:
- Frontend: HTML, Tailwind CSS, JavaScript
- Backend: Flask
- Database: SQLite

## Features
- Homepage with list of blog post summaries
- Blog detail page on click
- Admin interface to add or delete blog posts
- Attractive design with animations
- Responsive layout for all device sizes

## API Endpoints
- GET /api/blogs – List all blogs
- GET /api/blogs/{id} – View full blog content
- POST /api/blogs – Add a new blog
- DELETE /api/blogs/{id} – Delete blog

## Setup Instructions

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd blog_app
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   python init_db.py
   ```

### Running the Application

1. Start the Flask server:
   ```bash
   python run.py
   ```
   
   Or on Windows, you can simply run:
   ```bash
   setup.bat
   ```

2. Open your browser and visit:
   - http://localhost:5000 - Homepage
   - http://localhost:5000/admin - Admin panel

### Usage

- **Viewing Blogs**: Visit the homepage to see a list of blog post summaries. Click on "Read more" to view the full blog post.
- **Admin Panel**: Visit /admin to access the admin interface where you can:
  - Add new blog posts using the form on the left
  - Delete existing blog posts using the trash icon on the right

## Project Structure
```
blog_app/
│
├── app.py              # Flask application
├── run.py              # Application runner
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── setup.bat           # Windows setup script
├── README.md           # This file
├── blog.db             # SQLite database (created on first run)
│
├── templates/
│   ├── base.html       # Base template
│   ├── index.html      # Homepage
│   ├── blog.html       # Blog post page
│   └── admin.html      # Admin panel
│
└── static/             # Static files (if any)
```

## Technologies Used
- **Flask**: Web framework for Python
- **SQLite**: Lightweight database
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript**: Client-side interactivity
- **SweetAlert2**: Beautiful alert dialogs
- **Font Awesome**: Icon library

## Customization
You can customize the appearance by modifying the CSS in the base.html file or by adding new styles. The JavaScript files in each template can also be modified to change the behavior of the application.
"# blog-app" 
"# blog-app" 
