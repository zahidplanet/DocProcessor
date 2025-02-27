// DocProcessor JavaScript

// Initialize all Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-dismiss alerts
    const autoAlerts = document.querySelectorAll('.alert.auto-dismiss');
    autoAlerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // Dismiss after 5 seconds
    });
    
    // File input enhancements
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileNameDisplay = document.querySelector('.file-name');
            if (fileNameDisplay) {
                if (this.files && this.files.length > 0) {
                    fileNameDisplay.textContent = this.files[0].name;
                } else {
                    fileNameDisplay.textContent = 'No file selected';
                }
            }
        });
    }
    
    // Form validation example
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Document view page enhancements
function setupDocumentView() {
    const commentButtons = document.querySelectorAll('.add-comment-btn');
    commentButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('data-section');
            const commentForm = document.getElementById(`comment-form-${sectionId}`);
            if (commentForm) {
                commentForm.classList.toggle('d-none');
            }
        });
    });
}

// Comment management
function toggleCommentResolution(commentId) {
    const resolutionForm = document.getElementById(`resolution-form-${commentId}`);
    if (resolutionForm) {
        resolutionForm.classList.toggle('d-none');
    }
}

// Status update functions
function updateDocumentStatus(documentId, newStatus) {
    // This would be an AJAX call to update the status
    console.log(`Updating document ${documentId} to status: ${newStatus}`);
    // After success, update UI
    document.getElementById(`status-badge-${documentId}`).textContent = newStatus;
} 