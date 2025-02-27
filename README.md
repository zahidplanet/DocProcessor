# DocProcessor

A Python application for managing compliance and healthcare documentation review processes.

## Project Overview

DocProcessor is designed to streamline the process of handling healthcare compliance documentation and managing review comments from regulatory bodies like HCQC (Healthcare Quality and Compliance). The application helps healthcare organizations efficiently address and resolve comments across multiple document types such as Safety Risk Assessments, Functional Programs, and Equipment Lists.

## Key Features

- **Document Management**: Upload and organize compliance documentation
- **Comment Tracking**: Add, track, and resolve review comments
- **Cross-Document Reference**: Link related comments across multiple documents
- **Document Conversion**: Convert documents to editable formats as needed
- **Change Tracking**: Clearly visualize changes made between document versions
- **Approval Workflow**: Streamlined review and approval process
- **Changelog Generation**: Create formatted reports showing all modifications
- **Resubmission Ready**: Generate polished documents for regulatory resubmission

## Project Structure

```
DocProcessor/
├── src/                  # Source code
│   ├── core/             # Core application logic
│   ├── ui/               # User interface components
│   ├── utils/            # Utility functions and helpers
│   │   └── changelog/    # Changelog generation utilities
│   ├── templates/        # HTML templates
│   ├── static/           # Static assets (CSS, JS)
│   └── models/           # Data models and schemas
├── tests/                # Test suite
├── docs/                 # Documentation
└── README.md             # Project overview
```

## Development Roadmap

### Sprint 1: Project Setup and Core Functionality
- [x] Set up project structure and environment
- [x] Design data models for documents and comments
- [x] Implement document upload and parsing functionality
- [x] Create basic UI for document management

### Sprint 2: Comment Management
- [x] Implement comment tracking system
- [x] Develop cross-document reference functionality
- [x] Create comment resolution workflow
- [x] Build UI for comment management

### Sprint 3: Revision and Export
- [x] Implement document version control
- [x] Develop change tracking and visualization
- [x] Create export functionality with formatted changes
- [x] Build approval workflow

### Sprint 4: Polishing and Testing
- [x] Basic testing setup
- [ ] Comprehensive testing
- [ ] UI/UX improvements
- [ ] Documentation and user guides
- [ ] Final adjustments and bug fixes

## Getting Started

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/DocProcessor.git
   cd DocProcessor
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the application:
   ```
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Run the application:
   ```
   python -m src.app
   ```

6. Access the application in your browser at http://127.0.0.1:5000

## Features in Detail

### Changelog Generation

The application includes a powerful changelog generation system that can:

- Compare different versions of the same document
- Identify line-by-line changes (additions, deletions, modifications)
- Work with multiple document formats (PDF, Word, Excel)
- Include resolved comments in the changelog
- Generate formatted, human-readable reports

### Document Management

- Upload multiple document types
- Track document versions
- Manage document statuses throughout the review cycle

### Comment System

- Add comments to specific sections or pages
- Track comment resolution
- Link related comments across documents

## Requirements

- Python 3.8+
- Additional dependencies are listed in requirements.txt

## License

TBD 