import sqlite3
from datetime import datetime

# Database setup
DATABASE = 'blog.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author TEXT NOT NULL,
                date_created TEXT NOT NULL,
                summary TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                blog_id INTEGER NOT NULL,
                author_name TEXT NOT NULL,
                email TEXT,
                content TEXT NOT NULL,
                date_created TEXT NOT NULL,
                is_approved BOOLEAN DEFAULT 1,
                FOREIGN KEY (blog_id) REFERENCES blogs (id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        
        # Check if we already have data
        cursor.execute('SELECT COUNT(*) FROM blogs')
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert sample data
            sample_blogs = [
                (
                    'Getting Started with Flask',
                    'Flask is a lightweight WSGI web application framework. It is designed to make getting started very easy and quick, with the ability to scale up to complex applications.\n\nTo install Flask, you can use pip:\n\n```bash\npip install Flask\n```\n\nCreate a simple Flask application:\n\n```python\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef hello():\n    return "Hello, World!"\n\nif __name__ == "__main__":\n    app.run()\n```\n\nThis creates a simple web server that responds with "Hello, World!" when you visit the root URL.',
                    'Admin',
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Learn how to get started with Flask, a lightweight web framework for Python.'
                ),
                (
                    'Introduction to Tailwind CSS',
                    'Tailwind CSS is a utility-first CSS framework for rapidly building custom user interfaces. This guide will teach you how to get started with Tailwind CSS.\n\n## What is Tailwind CSS?\n\nTailwind CSS is a utility-first CSS framework that provides low-level utility classes to build designs without writing custom CSS.\n\n## Installation\n\nYou can install Tailwind CSS via npm:\n\n```bash\nnpm install tailwindcss\nnpx tailwindcss init\n```\n\n## Configuration\n\nCreate a `tailwind.config.js` file to configure Tailwind CSS:\n\n```javascript\nmodule.exports = {\n  content: ["./src/**/*.{html,js}"],\n  theme: {\n    extend: {},\n  },\n  plugins: [],\n}\n```\n\n## Usage\n\nAdd the Tailwind directives to your CSS:\n\n```css\n@tailwind base;\n@tailwind components;\n@tailwind utilities;\n```',
                    'Admin',
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Learn how to get started with Tailwind CSS, a utility-first CSS framework.'
                ),
                (
                    'JavaScript ES6 Features',
                    'ES6, also known as ECMAScript 2015, introduced many new features to JavaScript. Here are some of the most important ones:\n\n## Let and Const\n\nES6 introduced two new ways to declare variables: `let` and `const`.\n\n```javascript\n// var - function scoped\nvar x = 10;\n\n// let - block scoped\nlet y = 20;\n\n// const - block scoped, cannot be reassigned\nconst z = 30;\n```\n\n## Arrow Functions\n\nArrow functions provide a shorter syntax for writing functions:\n\n```javascript\n// ES5\nvar add = function(a, b) {\n  return a + b;\n};\n\n// ES6\nconst add = (a, b) => a + b;\n```\n\n## Template Literals\n\nTemplate literals allow embedded expressions:\n\n```javascript\nconst name = "John";\nconst greeting = `Hello, ${name}!`;\n```\n\n## Destructuring\n\nDestructuring allows you to extract values from arrays or objects:\n\n```javascript\nconst person = { name: "John", age: 30 };\nconst { name, age } = person;\n```',
                    'Admin',
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Explore the most important ES6 features that every JavaScript developer should know.'
                )
            ]
            
            cursor.executemany('''
                INSERT INTO blogs (title, content, author, date_created, summary)
                VALUES (?, ?, ?, ?, ?)
            ''', sample_blogs)
            
            conn.commit()
            print("Sample data inserted successfully!")
        else:
            print("Database already contains data. Skipping sample data insertion.")

if __name__ == '__main__':
    init_db()
