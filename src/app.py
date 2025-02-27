"""
Main application file for DocProcessor.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Initialize extensions
bootstrap = Bootstrap5(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html', title='DocProcessor Dashboard')

@app.route('/documents')
def documents():
    """Display list of uploaded documents."""
    # This will be implemented later
    return render_template('documents.html', title='Documents', documents=[])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle document uploads."""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        
        # If user does not select file, browser also
        # submits an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
            
        if file:
            # Process file upload - to be implemented
            flash('File uploaded successfully', 'success')
            return redirect(url_for('documents'))
            
    return render_template('upload.html', title='Upload Document')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True) 