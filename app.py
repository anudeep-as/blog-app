from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this_in_production'

# Database setup
DATABASE = 'blog.db'

# Authentication decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Admin login required to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Registration route
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username').strip()
#         password = request.form.get('password').strip()
#         if not username or not password:
#             flash('Username and password are required.', 'danger')
#             return render_template('registration.html')
#         password_hash = generate_password_hash(password)
#         created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         try:
#             with sqlite3.connect(DATABASE) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)',
#                                (username, password_hash, created_at))
#                 conn.commit()
#             flash('Registration successful. Please log in.', 'success')
#             return redirect(url_for('login'))
#         except sqlite3.IntegrityError:
#             flash('Username already exists. Please choose a different one.', 'danger')
#             return render_template('registration.html')
#         except Exception as e:
#             flash(f'An error occurred: {str(e)}', 'danger')
#             return render_template('registration.html')
#     return render_template('registration.html')

# Login route for admin
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Hardcoded admin credentials
        if username == 'admin' and password == 'password':
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Admin login successful.', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid admin username or password.', 'danger')
    return render_template('login.html')

# User login route
# @app.route('/user-login', methods=['GET', 'POST'])
# def user_login():
#     if request.method == 'POST':
#         username = request.form.get('username').strip()
#         password = request.form.get('password').strip()
#         with sqlite3.connect(DATABASE) as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
#             row = cursor.fetchone()
#             if row and check_password_hash(row[0], password):
#                 session['logged_in'] = True
#                 session['username'] = username
#                 flash('You were successfully logged in.', 'success')
#                 return redirect(url_for('index'))
#             else:
#                 flash('Invalid username or password.', 'danger')
#     return render_template('user_login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    session.pop('_flashes', None)
    flash('You were logged out.', 'info')
    return redirect(url_for('login'))

# Admin route
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blogs/<int:blog_id>')
def blog_detail(blog_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM blogs WHERE id = ?', (blog_id,))
        blog = cursor.fetchone()
        if blog:
            blog_dict = {
                'id': blog[0],
                'title': blog[1],
                'content': blog[2],
                'author': blog[3],
                'date_created': blog[4],
                'summary': blog[5]
            }
            return render_template('blog.html', blog=blog_dict)
        else:
            return "Blog not found", 404

@app.route('/api/blogs')
def get_blogs():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, author, date_created, summary FROM blogs ORDER BY date_created DESC')
        blogs = cursor.fetchall()
        blog_list = []
        for blog in blogs:
            blog_list.append({
                'id': blog[0],
                'title': blog[1],
                'author': blog[2],
                'date_created': blog[3],
                'summary': blog[4]
            })
        return jsonify(blog_list)

@app.route('/api/blogs/<int:blog_id>')
def get_blog(blog_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM blogs WHERE id = ?', (blog_id,))
        blog = cursor.fetchone()
        if blog:
            return jsonify({
                'id': blog[0],
                'title': blog[1],
                'content': blog[2],
                'author': blog[3],
                'date_created': blog[4],
                'summary': blog[5]
            })
        else:
            return jsonify({'error': 'Blog not found'}), 404

@app.route('/api/blogs', methods=['POST'])
@admin_login_required
def create_blog():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        author = data.get('author', 'Anonymous').strip()
        summary = data.get('summary', '').strip()
        
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400
        
        if not summary:
            summary = title[:100] + '...' if len(title) > 100 else title
        
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO blogs (title, content, author, date_created, summary)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, content, author, date_created, summary))
            conn.commit()
            blog_id = cursor.lastrowid
            
        return jsonify({
            'id': blog_id, 
            'message': 'Blog created successfully',
            'title': title,
            'author': author,
            'date_created': date_created
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blogs/<int:blog_id>', methods=['DELETE'])
@admin_login_required
def delete_blog(blog_id):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM blogs WHERE id = ?', (blog_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return jsonify({'message': 'Blog deleted successfully'})
            else:
                return jsonify({'error': 'Blog not found'}), 404
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Comments API endpoints
@app.route('/api/blogs/<int:blog_id>/comments', methods=['GET'])
def get_comments(blog_id):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, blog_id, author_name, email, content, date_created, is_approved 
                FROM comments 
                WHERE blog_id = ? AND is_approved = 1
                ORDER BY date_created DESC
            ''', (blog_id,))
            comments = cursor.fetchall()
            
            comment_list = []
            for comment in comments:
                comment_list.append({
                    'id': comment[0],
                    'blog_id': comment[1],
                    'author_name': comment[2],
                    'email': comment[3],
                    'content': comment[4],
                    'date_created': comment[5],
                    'is_approved': comment[6]
                })
            
            return jsonify(comment_list)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blogs/<int:blog_id>/comments', methods=['POST'])
def add_comment(blog_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        author_name = data.get('author_name', '').strip()
        email = data.get('email', '').strip()
        content = data.get('content', '').strip()
        
        if not author_name or not content:
            return jsonify({'error': 'Name and comment content are required'}), 400
            
        if len(content) < 5:
            return jsonify({'error': 'Comment must be at least 5 characters long'}), 400
            
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO comments (blog_id, author_name, email, content, date_created)
                VALUES (?, ?, ?, ?, ?)
            ''', (blog_id, author_name, email, content, date_created))
            conn.commit()
            
            return jsonify({
                'message': 'Comment added successfully',
                'id': cursor.lastrowid,
                'author_name': author_name,
                'date_created': date_created
            }), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@admin_login_required
def delete_comment(comment_id):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return jsonify({'message': 'Comment deleted successfully'})
            else:
                return jsonify({'error': 'Comment not found'}), 404
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get recent comments across all blogs
@app.route('/api/comments/recent', methods=['GET'])
def get_recent_comments():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT comments.id, comments.blog_id, comments.author_name, comments.content, comments.date_created, blogs.title
                FROM comments
                JOIN blogs ON comments.blog_id = blogs.id
                WHERE comments.is_approved = 1
                ORDER BY comments.date_created DESC
                LIMIT 10
            ''')
            comments = cursor.fetchall()
            comment_list = []
            for comment in comments:
                comment_list.append({
                    'id': comment[0],
                    'blog_id': comment[1],
                    'author_name': comment[2],
                    'content': comment[3],
                    'date_created': comment[4],
                    'blog_title': comment[5]
                })
            return jsonify(comment_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to add comment from home page
@app.route('/api/comments', methods=['POST'])
def add_comment_home():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        blog_id = data.get('blog_id')
        author_name = data.get('author_name', '').strip()
        content = data.get('content', '').strip()
        email = data.get('email', '').strip()

        if not blog_id or not author_name or not content:
            return jsonify({'error': 'Blog ID, name and comment content are required'}), 400

        if len(content) < 5:
            return jsonify({'error': 'Comment must be at least 5 characters long'}), 400

        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO comments (blog_id, author_name, email, content, date_created)
                VALUES (?, ?, ?, ?, ?)
            ''', (blog_id, author_name, email, content, date_created))
            conn.commit()

            return jsonify({
                'message': 'Comment added successfully',
                'id': cursor.lastrowid,
                'author_name': author_name,
                'date_created': date_created
            }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
