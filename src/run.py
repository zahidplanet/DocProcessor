"""
Main script to run the DocProcessor application.
"""

import os
from dotenv import load_dotenv
import argparse
import logging

from src.app import app


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Run the DocProcessor application')
    parser.add_argument('--host', type=str, default='127.0.0.1', 
                        help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=5000, 
                        help='Port to bind the server to')
    parser.add_argument('--debug', action='store_true', 
                        help='Enable debug mode')
    return parser.parse_args()


def main():
    """Main entry point for the application."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Set up logging
    setup_logging()
    
    # Parse command-line arguments
    args = parse_args()
    
    # Create upload directory if it doesn't exist
    upload_dir = os.environ.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Run the Flask application
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main() 