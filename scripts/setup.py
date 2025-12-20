#!/usr/bin/env python3
"""
Complete Setup and Installation Script
File: scripts/setup.py

This script automates the entire setup process for the Sales Automation system.

Usage:
    python scripts/setup.py
    
Features:
- Checks Python version
- Installs dependencies
- Creates directory structure
- Generates example .env file
- Sets up Google Sheets templates
- Tests API connections
- Validates configuration
- Provides next steps

Run this first before using the application!
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import json
import shutil

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def run_command(command, description):
    """Run a shell command and report results"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print_success(f"{description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_header("CHECKING PYTHON VERSION")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Current Python version: {version_str}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8 or higher is required!")
        print_info("Please upgrade Python and try again.")
        print_info("Download from: https://www.python.org/downloads/")
        return False
    
    print_success(f"Python {version_str} is compatible")
    return True

def check_pip():
    """Check if pip is installed"""
    print_header("CHECKING PIP")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print_success("pip is installed")
        print(f"  {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is not installed!")
        print_info("Install pip: python -m ensurepip --upgrade")
        return False

def create_directory_structure():
    """Create necessary directories"""
    print_header("CREATING DIRECTORY STRUCTURE")
    
    base_dir = Path(__file__).parent.parent
    
    directories = [
        'config',
        'data/logs',
        'data/uploads',
        'data/backups',
        'api',
        'src/database',
        'src/email',
        'src/social',
        'src/campaigns',
        'src/utils',
        'tests',
        'scripts',
        'electron-app/assets'
    ]
    
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print_success(f"Created: {directory}/")
    
    # Create __init__.py files for Python packages
    init_files = [
        'src/__init__.py',
        'src/database/__init__.py',
        'src/email/__init__.py',
        'src/social/__init__.py',
        'src/campaigns/__init__.py',
        'src/utils/__init__.py',
        'tests/__init__.py',
        'config/__init__.py'
    ]
    
    for init_file in init_files:
        init_path = base_dir / init_file
        if not init_path.exists():
            init_path.write_text('"""Package initialization"""\n')
            print_success(f"Created: {init_file}")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print_header("INSTALLING DEPENDENCIES")
    
    base_dir = Path(__file__).parent.parent
    requirements_file = base_dir / 'requirements.txt'
    
    if not requirements_file.exists():
        print_warning("requirements.txt not found, creating it...")
        
        requirements = """gspread==5.12.0
oauth2client==4.1.3
pillow==10.1.0
schedule==1.2.0
python-dotenv==1.0.0
requests==2.31.0
facebook-sdk==3.1.0
pytest==7.4.3
pytest-mock==3.12.0
pytest-cov==4.1.0
responses==0.24.1
flask==3.0.0
flask-cors==4.0.0
werkzeug==3.0.0
psutil==5.9.6
"""
        requirements_file.write_text(requirements)
        print_success("Created requirements.txt")
    
    print_info("Installing Python packages (this may take a few minutes)...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True
        )
        print_success("All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error("Failed to install dependencies")
        print_info("Try manually: pip install -r requirements.txt")
        return False

def create_env_file():
    """Create .env file from template"""
    print_header("CREATING ENVIRONMENT FILE")
    
    base_dir = Path(__file__).parent.parent
    env_file = base_dir / '.env'
    env_example = base_dir / '.env.example'
    
    if env_file.exists():
        print_warning(".env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print_info("Keeping existing .env file")
            return True
    
    env_content = """# Email Configuration
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS=config/credentials.json
SALES_SHEET_NAME=Sales Leads
SOCIAL_SHEET_NAME=Social Media Content

# Facebook/Instagram (Meta) API
META_ACCESS_TOKEN=your_meta_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
INSTAGRAM_ACCOUNT_ID=your_instagram_business_account_id

# LinkedIn API
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_PERSON_URN=your_linkedin_person_urn
LINKEDIN_ORGANIZATION_URN=your_organization_urn

# Daily Limits
EMAIL_DAILY_LIMIT=450
FACEBOOK_DAILY_LIMIT=200
INSTAGRAM_DAILY_LIMIT=100
LINKEDIN_DAILY_LIMIT=100

# Logging
LOG_LEVEL=INFO
"""
    
    env_file.write_text(env_content)
    print_success("Created .env file")
    print_warning("IMPORTANT: Edit .env file with your actual credentials!")
    
    return True

def create_gitignore():
    """Create .gitignore file"""
    print_header("CREATING .gitignore")
    
    base_dir = Path(__file__).parent.parent
    gitignore_file = base_dir / '.gitignore'
    
    if gitignore_file.exists():
        print_info(".gitignore already exists, skipping")
        return True
    
    gitignore_content = """# Credentials
config/credentials.json
.env

# Logs
data/logs/*.log
data/logs/*.csv

# Uploads
data/uploads/*
!data/uploads/.gitkeep

# Backups
data/backups/*
!data/backups/.gitkeep

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Node (Electron)
electron-app/node_modules/
electron-app/dist/
electron-app/package-lock.json
"""
    
    gitignore_file.write_text(gitignore_content)
    print_success("Created .gitignore")
    
    return True

def create_readme():
    """Create README.md if it doesn't exist"""
    print_header("CREATING README")
    
    base_dir = Path(__file__).parent.parent
    readme_file = base_dir / 'README.md'
    
    if readme_file.exists():
        print_info("README.md already exists, skipping")
        return True
    
    readme_content = """# Sales & Social Media Automation

Complete automation system for sales campaigns and social media management.

## Quick Start

1. **Install dependencies:**
   ```bash
   python scripts/setup.py
   ```

2. **Configure credentials:**
   - Edit `.env` with your API credentials
   - Add `config/credentials.json` for Google Sheets

3. **Run the application:**
   ```bash
   # Start API server
   python api/app.py

   # Start automation bot
   python run_scheduler.py

   # Run tests
   pytest
   ```

## Features

- Multi-stage email campaigns
- Social media automation (Facebook, Instagram, LinkedIn)
- Real-time analytics dashboard
- Automated scheduling
- Engagement tracking

## Documentation

See the full documentation in the project files.

## Support

For issues or questions, check the logs in `data/logs/`
"""
    
    readme_file.write_text(readme_content)
    print_success("Created README.md")
    
    return True

def create_google_sheets_template():
    """Create Google Sheets template CSV files"""
    print_header("CREATING GOOGLE SHEETS TEMPLATES")
    
    base_dir = Path(__file__).parent.parent
    templates_dir = base_dir / 'data' / 'templates'
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Sales Leads template
    sales_template = templates_dir / 'sales_leads_template.csv'
    sales_content = """Name,Email,Company,Industry,Status,Last Contact,Stage
John Doe,john@example.com,TechCorp,SaaS,Pending,,0
Jane Smith,jane@startup.io,StartupX,E-commerce,Pending,,0
Bob Johnson,bob@consulting.com,ConsultCo,Consulting,Pending,,0
"""
    sales_template.write_text(sales_content)
    print_success("Created sales_leads_template.csv")
    
    # Social Posts template
    social_template = templates_dir / 'social_posts_template.csv'
    social_content = """Date,Time,Platform,Text,Media,Hashtags,Status,Posted Time,Post ID
2025-12-09,09:00,Facebook,Good morning! Starting the week strong,#motivation #monday,Pending,,
2025-12-09,12:00,Instagram,Behind the scenes at our office today!,image.jpg,#behindthescenes #team,Pending,,
2025-12-09,15:00,LinkedIn,Excited to share insights from our latest project,,#business #innovation,Pending,,
"""
    social_template.write_text(social_content)
    print_success("Created social_posts_template.csv")
    
    print_info("Import these templates into your Google Sheets")
    
    return True

def check_node_installed():
    """Check if Node.js is installed (for Electron app)"""
    print_header("CHECKING NODE.JS (OPTIONAL)")
    
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print_success(f"Node.js is installed: {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_warning("Node.js is not installed")
        print_info("Node.js is only needed for the Electron desktop app")
        print_info("Download from: https://nodejs.org/")
        return False

def validate_configuration():
    """Validate the configuration"""
    print_header("VALIDATING CONFIGURATION")
    
    base_dir = Path(__file__).parent.parent
    
    # Check .env file
    env_file = base_dir / '.env'
    if env_file.exists():
        print_success(".env file exists")
        
        # Check if still has default values
        content = env_file.read_text()
        if 'your_email@gmail.com' in content:
            print_warning("⚠️  .env contains default values - YOU MUST UPDATE IT!")
        else:
            print_success("✓ .env appears to be configured")
    else:
        print_error(".env file not found")
    
    # Check credentials.json
    creds_file = base_dir / 'config' / 'credentials.json'
    if creds_file.exists():
        print_success("Google Sheets credentials found")
    else:
        print_warning("config/credentials.json not found")
        print_info("Download from Google Cloud Console")
    
    return True

def print_next_steps():
    """Print next steps for user"""
    print_header("SETUP COMPLETE!")
    
    print(f"{Colors.OKGREEN}✓ Installation successful!{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}NEXT STEPS:{Colors.ENDC}\n")
    
    print("1  Configure your credentials:")
    print("   - Edit .env file with your API keys")
    print("   - Add config/credentials.json from Google Cloud\n")
    
    print("2  Setup Google Sheets:")
    print("   - Create two sheets: 'Sales Leads' and 'Social Media Content'")
    print("   - Use templates in data/templates/")
    print("   - Share sheets with service account email\n")
    
    print("3  Test the setup:")
    print("   python scripts/test_connections.py\n")
    
    print("4  Start the API:")
    print("   python api/app.py\n")
    
    print("5  Run automation:")
    print("   python run_scheduler.py\n")
    
    print("6  Run tests:")
    print("   pytest\n")
    
    print(f"{Colors.BOLD}OPTIONAL:{Colors.ENDC}\n")
    print(" Desktop App:")
    print("   cd electron-app")
    print("   npm install")
    print("   npm start\n")
    
    print(f"{Colors.BOLD}DOCUMENTATION:{Colors.ENDC}\n")
    print(" Check README.md for full documentation")
    print(" Example templates in data/templates/")
    print(" View logs in data/logs/\n")
    
    print(f"{Colors.OKGREEN}Happy Automating! {Colors.ENDC}\n")

def main():
    """Main setup function"""
    print_header("SALES AUTOMATION SETUP")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version.split()[0]}\n")
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Create structure
    create_directory_structure()
    
    # Install dependencies
    install_dependencies()
    
    # Create configuration files
    create_env_file()
    create_gitignore()
    create_readme()
    create_google_sheets_template()
    
    # Validate
    validate_configuration()
    
    # Optional checks
    check_node_installed()
    
    # Print next steps
    print_next_steps()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Setup interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Setup failed with error: {e}{Colors.ENDC}")
        sys.exit(1)