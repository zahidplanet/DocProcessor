"""
Main application file for DocProcessor.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename

from src.models.document import DocumentType, DocumentStatus, CommentStatus
from src.core.document_manager import DocumentManager
from src.core.comment_manager import CommentManager
from src.utils.changelog.generator import ChangelogGenerator

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Initialize extensions
bootstrap = Bootstrap5(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize managers
document_manager = DocumentManager(app.config['UPLOAD_FOLDER'])
comment_manager = CommentManager()
changelog_generator = ChangelogGenerator(app.config['UPLOAD_FOLDER'])

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'xlsx', 'xls'}

def allowed_file(filename):
    """Check if a filename has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html', title='DocProcessor Dashboard')

@app.route('/documents')
def documents():
    """Display list of uploaded documents."""
    all_documents = document_manager.get_all_documents()
    return render_template('documents.html', title='Documents', documents=all_documents)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle document uploads."""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
            
        file = request.files['file']
        
        # If user does not select file, browser also
        # submits an empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        document_type_str = request.form.get('document_type')
        if not document_type_str:
            flash('Please select a document type', 'danger')
            return redirect(request.url)
        
        try:
            document_type = DocumentType(document_type_str)
        except ValueError:
            flash('Invalid document type', 'danger')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            try:
                # Upload document
                document = document_manager.upload_document(
                    file.stream, 
                    secure_filename(file.filename),
                    document_type
                )
                flash(f'Document "{file.filename}" uploaded successfully', 'success')
                return redirect(url_for('document_detail', document_id=document.id))
            except Exception as e:
                app.logger.error(f"Error uploading document: {str(e)}")
                flash(f'Error uploading document: {str(e)}', 'danger')
                return redirect(request.url)
        else:
            flash('Invalid file type. Allowed types: PDF, Word (DOCX/DOC), Excel (XLSX/XLS)', 'danger')
            return redirect(request.url)
            
    return render_template('upload.html', title='Upload Document')

@app.route('/documents/<document_id>')
def document_detail(document_id):
    """Display document details and comments."""
    try:
        document = document_manager.get_document(document_id)
        comments = comment_manager.get_comments_for_document(document_id)
        return render_template(
            'document_detail.html',
            title=f'Document: {document.original_filename}',
            document=document,
            comments=comments
        )
    except KeyError:
        flash('Document not found', 'danger')
        return redirect(url_for('documents'))

@app.route('/downloads/<document_id>')
def download_document(document_id):
    """Download a document."""
    try:
        document = document_manager.get_document(document_id)
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            document.filename,
            as_attachment=True,
            download_name=document.original_filename
        )
    except KeyError:
        flash('Document not found', 'danger')
        return redirect(url_for('documents'))

@app.route('/documents/<document_id>/add_comment', methods=['POST'])
def add_comment(document_id):
    """Add a comment to a document."""
    try:
        document_manager.get_document(document_id)  # Ensure document exists
        
        text = request.form.get('text')
        if not text:
            flash('Comment text is required', 'danger')
            return redirect(url_for('document_detail', document_id=document_id))
        
        page_number = request.form.get('page_number')
        if page_number:
            try:
                page_number = int(page_number)
            except ValueError:
                page_number = None
        
        section = request.form.get('section')
        
        comment = comment_manager.add_comment(
            document_id=document_id,
            text=text,
            page_number=page_number,
            section=section
        )
        
        # Update document status if this is the first comment
        document = document_manager.get_document(document_id)
        if document.status == DocumentStatus.UPLOADED:
            document_manager.update_document_status(document_id, DocumentStatus.IN_REVIEW)
        
        flash('Comment added successfully', 'success')
        return redirect(url_for('document_detail', document_id=document_id))
    except KeyError:
        flash('Document not found', 'danger')
        return redirect(url_for('documents'))

@app.route('/comments/<comment_id>/resolve', methods=['POST'])
def resolve_comment(comment_id):
    """Resolve a comment."""
    try:
        comment = comment_manager.get_comment(comment_id)
        document_id = comment.document_id
        
        resolution_text = request.form.get('resolution_text')
        if not resolution_text:
            flash('Resolution text is required', 'danger')
            return redirect(url_for('document_detail', document_id=document_id))
        
        # In a real app, we would get the current user
        resolved_by = "System User"
        
        # Resolve the comment
        comment_manager.resolve_comment(comment_id, resolution_text, resolved_by)
        
        # Check if all comments for this document are resolved
        open_comments = comment_manager.get_open_comments_for_document(document_id)
        if not open_comments:
            # All comments resolved, update document status
            document_manager.update_document_status(document_id, DocumentStatus.REVIEWED)
        
        flash('Comment resolved successfully', 'success')
        return redirect(url_for('document_detail', document_id=document_id))
    except KeyError:
        flash('Comment not found', 'danger')
        return redirect(url_for('documents'))

@app.route('/documents/<document_id>/update_status', methods=['POST'])
def update_document_status(document_id):
    """Update the status of a document."""
    try:
        status_str = request.form.get('status')
        if not status_str:
            flash('Status is required', 'danger')
            return redirect(url_for('document_detail', document_id=document_id))
        
        try:
            status = DocumentStatus(status_str)
        except ValueError:
            flash('Invalid document status', 'danger')
            return redirect(url_for('document_detail', document_id=document_id))
        
        document = document_manager.update_document_status(document_id, status)
        
        flash(f'Document status updated to {status.value}', 'success')
        return redirect(url_for('document_detail', document_id=document_id))
    except KeyError:
        flash('Document not found', 'danger')
        return redirect(url_for('documents'))

@app.route('/documents/<document_id>/new_version', methods=['GET', 'POST'])
def upload_new_version(document_id):
    """Upload a new version of a document."""
    try:
        original_document = document_manager.get_document(document_id)
        
        if request.method == 'POST':
            # Check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
                
            file = request.files['file']
            
            # If user does not select file, browser also
            # submits an empty part without filename
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
                
            if file and allowed_file(file.filename):
                try:
                    # Upload new version
                    new_document = document_manager.create_new_version(
                        document_id,
                        file.stream
                    )
                    
                    flash(f'New version of "{original_document.original_filename}" uploaded successfully', 'success')
                    return redirect(url_for('document_detail', document_id=new_document.id))
                except Exception as e:
                    app.logger.error(f"Error uploading new version: {str(e)}")
                    flash(f'Error uploading new version: {str(e)}', 'danger')
                    return redirect(url_for('document_detail', document_id=document_id))
            else:
                flash('Invalid file type. Allowed types: PDF, Word (DOCX/DOC), Excel (XLSX/XLS)', 'danger')
                return redirect(url_for('document_detail', document_id=document_id))
                
        return render_template(
            'upload_new_version.html',
            title=f'Upload New Version: {original_document.original_filename}',
            document=original_document
        )
    except KeyError:
        flash('Document not found', 'danger')
        return redirect(url_for('documents'))

@app.route('/documents/<document_id>/changelog')
def view_changelog(document_id):
    """View changelog between document versions."""
    try:
        document = document_manager.get_document(document_id)
        
        # If this is not a versioned document, check if it has versions
        if not document.parent_document_id:
            # Get all versions (children) of this document
            versions = document_manager.get_document_versions(document_id)
            if not versions:
                flash('No versions available for this document', 'warning')
                return redirect(url_for('document_detail', document_id=document_id))
                
            # Use the newest version for comparison
            newest_version = max(versions, key=lambda d: d.version)
            return redirect(url_for('view_changelog_between_versions', 
                                   original_id=document_id, 
                                   new_id=newest_version.id))
        
        # If this is a versioned document, compare with parent
        parent_id = document.parent_document_id
        return redirect(url_for('view_changelog_between_versions', 
                               original_id=parent_id, 
                               new_id=document_id))
    except KeyError:
        flash('Document not found', 'danger')
        return redirect(url_for('documents'))

@app.route('/changelog/<original_id>/<new_id>')
def view_changelog_between_versions(original_id, new_id):
    """View changelog between two specific document versions."""
    try:
        original_doc = document_manager.get_document(original_id)
        new_doc = document_manager.get_document(new_id)
        
        # Get resolved comments for the original document
        all_comments = comment_manager.get_comments_for_document(original_id)
        resolved_comments = [c for c in all_comments if c.status == CommentStatus.RESOLVED]
        
        # Generate changelog
        formatted_changelog = changelog_generator.generate_formatted_changelog(
            original_doc, new_doc, resolved_comments
        )
        
        return render_template(
            'changelog.html',
            title=f'Changelog: {original_doc.original_filename}',
            original_doc=original_doc,
            new_doc=new_doc,
            changelog=formatted_changelog
        )
    except KeyError as e:
        flash(f'Document not found: {str(e)}', 'danger')
        return redirect(url_for('documents'))
    except Exception as e:
        app.logger.error(f"Error generating changelog: {str(e)}")
        flash(f'Error generating changelog: {str(e)}', 'danger')
        return redirect(url_for('documents'))

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